from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from product.models import Item
from django.db.models import  F, ExpressionWrapper, FloatField, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from product.filters import ItemFilter
import json
from datetime import datetime, date
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd


class DemandForecastView(LoginRequiredMixin, FilterView):
    model = Item
    filterset_class = ItemFilter
    template_name = 'analytics/demand_forecast.html'

    def get_queryset(self):
        queryset = super().get_queryset()  # Получите исходный queryset
        # Примените фильтр, если он был отправлен в запросе
        self.filterset = ItemFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs  # Верните отфильтрованный queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        items = (
            queryset.filter(sold=True)
            .values('sales_date')
            .annotate(
                total_price=Sum(ExpressionWrapper(F('quantity') * F('sales_price'), output_field=FloatField())),
                total_profit=Sum(ExpressionWrapper(F('quantity') * (F('sales_price') - F('purchase_price')), output_field=FloatField())),
                total_quantity=Sum(F('quantity')),
            )
            .order_by('sales_date')
        )
        
         # Обработка и подготовка данных
        data = {'sales_date': [], 'total_quantity': []} #, 'total_profit': [], 'total_price': [], }
        for item in items:
       
            data['sales_date'].append(item['sales_date'])
            data['total_quantity'].append(item['total_quantity'])
            # data['total_profit'].append(item['total_profit'])
            # data['total_price'].append(item['total_price'])
    
        df = pd.DataFrame(data)
        df['sales_date'] = pd.to_datetime(df['sales_date'])
        df = df.set_index('sales_date')
        # Ресемплирование данных с ежедневной периодичностью и заполнение недостающих дней нулями
        df = df.resample('D').sum().fillna(0)
        
        print('df',df)
        # Прогнозирование спроса
        model = ARIMA(df['total_quantity'], order=(5,1,0))
        results = model.fit()
    
        forecast_dates = pd.date_range(start=df.index[-1], periods=31, freq='D')[1:]

        # Прогнозируем спрос
        forecast_values = results.forecast(steps=30)
        # Округляем прогнозируемые значения до целых чисел
        forecast_values_rounded = forecast_values.round().astype(int)

        # Преобразуем индекс в список строковых представлений дат
        forecast_dates_str = forecast_dates.strftime('%Y-%m-%d').tolist()

        sales_date_list = df.index.tolist()
        print('sales_date_list',sales_date_list)
        charts_data = dict()
        charts_data['cost_chart'] = dict()
        charts_data['cost_chart']['dades_list'] = forecast_dates_str
        charts_data['cost_chart']['series'] = [
            {'name': 'прогноз', 'data': forecast_values_rounded.tolist()},
        ]
       

        def custom_serializer(obj):
            if isinstance(obj, (datetime, date)):
                serial = obj.isoformat()
                return serial

        json_charts_data = json.dumps(charts_data, default=custom_serializer)

        context['charts_data'] = json_charts_data
        return context


class SalesView(LoginRequiredMixin, FilterView):
    model = Item
    filterset_class = ItemFilter
    template_name = 'analytics/sales.html'

    def get_queryset(self):
        queryset = super().get_queryset()  # Получите исходный queryset
        # Примените фильтр, если он был отправлен в запросе
        self.filterset = ItemFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs  # Верните отфильтрованный queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        items = (
            queryset.filter(sold=True)
            .values('sales_date')
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
            queryset.filter(sold=False)
            .values('purchase_date')
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


class MixedView(LoginRequiredMixin, FilterView):
    model = Item
    filterset_class = ItemFilter
    template_name = 'analytics/mixed.html'

    def get_queryset(self):
        queryset = super().get_queryset()  # Получите исходный queryset

        # Примените фильтр, если он был отправлен в запросе
        self.filterset = ItemFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs  # Верните отфильтрованный queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        items2 = (
            queryset.filter(sold=False)
            .values('purchase_date')
            .annotate(
                received_total_price=Sum(ExpressionWrapper(F('quantity') * F('purchase_price'), output_field=FloatField())),
                received_total_quantity =Sum(F('quantity')),
            )
            .order_by('purchase_date')
        )
        items1 = (
            queryset.filter(sold=True)
            .values('sales_date')
            .annotate(
                sales_total_price=Sum(ExpressionWrapper(F('quantity') * F('sales_price'), output_field=FloatField())),
                sales_total_quantity=Sum(F('quantity')),
                
            )
            .order_by('sales_date')
        )
        
        
        # Обработка и подготовка данных
        data1 = {'date_list': [], 'all_sales_total_price_list': [], 'all_sales_total_quantity_list': []}
        for item in items1:
        
            data1['date_list'].append(item['sales_date'])
            data1['all_sales_total_price_list'].append(item['sales_total_price'])
            data1['all_sales_total_quantity_list'].append(item['sales_total_quantity'])

        data2 = {'date_list': [], 'all_received_total_price_list': [], 'all_received_total_quantity_list': []}
        for item in items2:
        
            data2['date_list'].append(item['purchase_date'])
            data2['all_received_total_price_list'].append(item['received_total_price'])
            data2['all_received_total_quantity_list'].append(item['received_total_quantity'])

        # Создание DataFrame
        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data2)

        # Объединение по столбцу с датой
        merged_df = pd.merge(df1, df2, on='date_list', how='outer')
        
        merged_df['date_list'] = pd.to_datetime(merged_df['date_list'])
        merged_df['date_list'] = merged_df['date_list'].dt.date
        merged_df = merged_df.set_index('date_list')
        
        # merged_df = merged_df.resample('D').sum().fillna(0)
        # print('merged_df2',merged_df)
        # Преобразование DataFrame в списки
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