
from item.models import Item, SalesItem
from django.db.models import  F, ExpressionWrapper, FloatField, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.views.generic import TemplateView
from item.filters import ItemFilter, SalesItemFilter
from .forms import DateRangeForm
import json

from datetime import datetime, date
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

# Импортируем необходимую функцию
from sklearn.metrics import mean_squared_error, mean_absolute_error


class DemandForecastView(LoginRequiredMixin, FilterView):
    model = SalesItem
    filterset_class = SalesItemFilter
    template_name = 'analytics/demand_forecast.html'

    def get_queryset(self):
        queryset = super().get_queryset()  # Получите исходный queryset
        # Примените фильтр, если он был отправлен в запросе
        self.filterset = SalesItemFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs  # Верните отфильтрованный queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()


        items = (
            queryset.values('sales_date')
            .annotate(
                total_quantity=Sum(F('quantity')),
            )
            .order_by('sales_date')
        )

        data = {'sales_date': [], 'total_quantity': [] }
        for item in items:
       
            data['sales_date'].append(item['sales_date'])
            data['total_quantity'].append(item['total_quantity'])
       
        print('data',data)
        df = pd.DataFrame(data)
        
        df['sales_date'] = pd.to_datetime(df['sales_date'])
        df = df.set_index('sales_date')
        # Ресемплирование данных с ежедневной периодичностью и заполнение недостающих дней нулями
        df = df.resample('D').sum().fillna(0)
        print('df',df)


        model = ARIMA(df['total_quantity'], order=(3,1,1))
        model_fit = model.fit()
       
       
        
        steps = 7
        # Прогноз на основе обученной модели
        forecast = model_fit.forecast(steps=steps)

        # Рассчитываем MSE и MAE
        mse = mean_squared_error(df['total_quantity'][-steps:], forecast)
        mae = mean_absolute_error(df['total_quantity'][-steps:], forecast)

        print(f'MSE: {mse}')
        print(f'MAE: {mae}')
        
        # Создаем новый DataFrame для будущих значений
        future_dates = pd.date_range(start=df.index[-steps-1], periods=steps*2, freq='D') + pd.DateOffset(days=1)
        
        # Округляем прогнозируемые значения до целых чисел
        forecast_values_rounded = forecast.round().astype(int)

        # Преобразуем индекс в список строковых представлений дат
        forecast_dates_str = future_dates.strftime('%Y-%m-%d').tolist()

        
        nul_list = [None] * 7
        
        
        charts_data = dict()
        charts_data['cost_chart'] = dict()
        charts_data['cost_chart']['dades_list'] = forecast_dates_str
        charts_data['cost_chart']['series'] = [
            {'name': 'прогноз прошлые 7 дней', 'data': df['total_quantity'][-steps:].tolist() + nul_list},
            {'name': 'прогноз на 7 дней', 'data': nul_list + forecast_values_rounded.tolist()},
        ]
       

        def custom_serializer(obj):
            if isinstance(obj, (datetime, date)):
                serial = obj.isoformat()
                return serial

        json_charts_data = json.dumps(charts_data, default=custom_serializer)

        context['charts_data'] = json_charts_data
        return context


class SalesView(LoginRequiredMixin, FilterView):
    model = SalesItem
    filterset_class = SalesItemFilter
    template_name = 'analytics/sales.html'

    def get_queryset(self):
        queryset = super().get_queryset()  # Получите исходный queryset
        # Примените фильтр, если он был отправлен в запросе
        self.filterset = SalesItemFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs  # Верните отфильтрованный queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        items = (
            queryset.values('sales_date')
            .annotate(
                total_price=Sum(ExpressionWrapper(F('quantity') * F('sales_price'), output_field=FloatField())),
                total_profit=Sum(ExpressionWrapper(F('quantity') * (F('sales_price') - F('purchase_price')), output_field=FloatField())),
                total_quantity=Sum(F('quantity')),
                
            )
            .order_by('sales_date')
        )
        
        # Обработка и подготовка данных
        data = {'sales_date_list': [], 'all_total_price_list': [], 'all_total_profit_list': [], 'all_total_quantity_list': []}
        for item in items:
        
            data['sales_date_list'].append(item['sales_date'])
            data['all_total_price_list'].append(item['total_price'])
            data['all_total_profit_list'].append(item['total_profit'])
            data['all_total_quantity_list'].append(item['total_quantity'])

        
        df = pd.DataFrame(data)
        df['sales_date_list'] = pd.to_datetime(df['sales_date_list'])
        df['sales_date_list'] = df['sales_date_list'].dt.date
        df = df.set_index('sales_date_list')
        print('df',df)
        # Преобразование DataFrame в списки
        sales_date_list = df.index.tolist()
        print('sales_date_list',sales_date_list)
        charts_data = dict()
        charts_data['cost_chart'] = dict()
        charts_data['cost_chart']['dades_list'] = sales_date_list
        charts_data['cost_chart']['series'] = [
            {'name': 'Сбыто в (BYN)', 'data': df['all_total_price_list'].tolist()},
            {'name': 'Прыбыль в (BYN)', 'data': df['all_total_profit_list'].tolist()},
           
        ]
        charts_data['quantity_chart'] = dict()
        charts_data['quantity_chart']['dades_list'] = sales_date_list
        charts_data['quantity_chart']['series'] = [
            {'name': 'Сбыто', 'data': df['all_total_quantity_list'].tolist()},
            
        ]

        def custom_serializer(obj):
            if isinstance(obj, (datetime, date)):
                serial = obj.isoformat()
                return serial

        json_charts_data = json.dumps(charts_data, default=custom_serializer)

        context['charts_data'] = json_charts_data
        return context


class FuncView(LoginRequiredMixin, FilterView):
    model = Item
    filterset_class = ItemFilter
    template_name = 'analytics/main.html'

    def get_queryset(self):
        queryset = super().get_queryset()  # Получите исходный queryset

        # Примените фильтр, если он был отправлен в запросе
        self.filterset = ItemFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs  # Верните отфильтрованный queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        items = (
            queryset.values('purchase_date')
            .annotate(
                received_price=Sum(ExpressionWrapper(F('quantity') * F('purchase_price'), output_field=FloatField())),
                remainder_price=Sum(ExpressionWrapper((F('quantity') - F('soldQuantity')) * F('purchase_price'), output_field=FloatField())),
                received=Sum(F('quantity')),
                remainder=Sum(F('quantity') - F('soldQuantity'))
            )
            .order_by('purchase_date')
        )
        
        # Обработка и подготовка данных
        data = {'dades_list': [], 'all_received_price_list': [], 'all_remainder_price_list': [], 'all_received_list': [], 'all_remainder_list': []}
        for item in items:
        
            data['dades_list'].append(item['purchase_date'])
            data['all_received_price_list'].append(item['received_price'])
            data['all_remainder_price_list'].append(item['remainder_price'])
            data['all_received_list'].append(item['received'])
            data['all_remainder_list'].append(item['remainder'])

        
        df = pd.DataFrame(data)
        df['dades_list'] = pd.to_datetime(df['dades_list'])
        df['dades_list'] = df['dades_list'].dt.date
        df = df.set_index('dades_list')
        print('df',df)
        # Преобразование DataFrame в списки
        dades_list = df.index.tolist()
        print('dades_list',dades_list)
        charts_data = dict()
        charts_data['cost_chart'] = dict()
        charts_data['cost_chart']['dades_list'] = dades_list
        charts_data['cost_chart']['series'] = [
            {'name': 'Поступления в (BYN)', 'data': df['all_received_price_list'].tolist()},
            {'name': 'Осталось в (BYN)', 'data': df['all_remainder_price_list'].tolist()},
        ]
        charts_data['quantity_chart'] = dict()
        charts_data['quantity_chart']['dades_list'] = dades_list
        charts_data['quantity_chart']['series'] = [
            {'name': 'Поступления', 'data': df['all_received_list'].tolist()},
            {'name': 'Осталось', 'data': df['all_remainder_list'].tolist()},
        ]

        def custom_serializer(obj):
            if isinstance(obj, (datetime, date)):
                serial = obj.isoformat()
                return serial

        json_charts_data = json.dumps(charts_data, default=custom_serializer)

        context['charts_data'] = json_charts_data
        return context


class MixedView(LoginRequiredMixin, TemplateView):
    
   
    template_name = 'analytics/mixed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DateRangeForm(self.request.GET)
        items = Item.objects.all()
        sales_items = SalesItem.objects.all()

        if form.is_valid():
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            if date_from:
                items = items.filter(purchase_date__gte=date_from)
                sales_items = sales_items.filter(sales_date__gte=date_from)
            if date_to:
                items = items.filter(purchase_date__lte=date_to)
                sales_items = sales_items.filter(sales_date__lte=date_to)
            
        context['form'] = form
        
        sales_items = (sales_items
                        .values('sales_date')
                        .annotate(
                            sales_total_price=Sum(ExpressionWrapper(F('quantity') * F('sales_price'), output_field=FloatField())), 
                            sales_total_quantity=Sum(F('quantity')),)
                        .order_by('sales_date'))
        
        items = (items
                    .values('purchase_date')
                    .annotate(
                        received_total_price=Sum(ExpressionWrapper(F('quantity') * F('purchase_price'), output_field=FloatField())),
                        received_total_quantity =Sum(F('quantity')),
                    )
                    .order_by('purchase_date'))
        
        # Обработка и подготовка данных
        sales_items_data = {'date_list': [], 'all_sales_total_price_list': [], 'all_sales_total_quantity_list': []}
        for item in sales_items:
        
            sales_items_data['date_list'].append(item['sales_date'])
            sales_items_data['all_sales_total_price_list'].append(item['sales_total_price'])
            sales_items_data['all_sales_total_quantity_list'].append(item['sales_total_quantity'])

        items_data = {'date_list': [], 'all_received_total_price_list': [], 'all_received_total_quantity_list': []}
        for item in items:
        
            items_data['date_list'].append(item['purchase_date'])
            items_data['all_received_total_price_list'].append(item['received_total_price'])
            items_data['all_received_total_quantity_list'].append(item['received_total_quantity'])

        # Создание DataFrame
        df1 = pd.DataFrame(sales_items_data)
        df2 = pd.DataFrame(items_data)

        # Объединение по столбцу с датой
        merged_df = pd.merge(df1, df2, on='date_list', how='outer')
        
        merged_df['date_list'] = pd.to_datetime(merged_df['date_list'])
        merged_df['date_list'] = merged_df['date_list'].dt.date
        merged_df = merged_df.set_index('date_list')
        
        
        sales_date_list = merged_df.index.tolist()
        print('sales_date_list',sales_date_list)
        charts_data = dict()
        charts_data['cost_chart'] = dict()
        charts_data['cost_chart']['dades_list'] = sales_date_list
        charts_data['cost_chart']['series'] = [
            {'name': 'Сбыто в (BYN)', 'data': merged_df['all_sales_total_price_list'].tolist()},
            {'name': 'Поступило в (BYN)', 'data': merged_df['all_received_total_price_list'].tolist()},
        
        ]
        charts_data['quantity_chart'] = dict()
        charts_data['quantity_chart']['dades_list'] = sales_date_list
        charts_data['quantity_chart']['series'] = [
            {'name': 'Сбыто', 'data': merged_df['all_sales_total_quantity_list'].tolist()},
            {'name': 'Поступило', 'data': merged_df['all_received_total_quantity_list'].tolist()},
            
        ]

        def custom_serializer(obj):
            if isinstance(obj, (datetime, date)):
                serial = obj.isoformat()
                return serial

        json_charts_data = json.dumps(charts_data, default=custom_serializer)

        context['charts_data'] = json_charts_data
       
        return context