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

def demand_forecast(request):
    # Получаем данные для прогнозирования спроса
    items = Item.objects.filter(sold=True).values('sales_date').annotate(total_sales=Sum('quantity')).order_by('sales_date')

    print('items',items)
    
    # Обработка и подготовка данных
    data = {'sales_date': [], 'total_sales': []}
    for item in items:
       
        data['sales_date'].append(item['sales_date'])
        data['total_sales'].append(item['total_sales'])
    
    df = pd.DataFrame(data)
    df['sales_date'] = pd.to_datetime(df['sales_date'])
    df = df.set_index('sales_date')
    # Ресемплирование данных с ежедневной периодичностью и заполнение недостающих дней нулями
    df = df.resample('D').sum().fillna(0)
    
    print('df',df)
    # Прогнозирование спроса
    model = ARIMA(df['total_sales'], order=(5,1,0))
    results = model.fit()
    # Генерируем даты для прогноза на 12 месяцев вперед
    forecast_dates = pd.date_range(start=df.index[-1], periods=31, freq='D')[1:]

    # Прогнозируем спрос
    forecast_values = results.forecast(steps=30)
    # Округляем прогнозируемые значения до целых чисел
    forecast_values_rounded = forecast_values.round().astype(int)

    # Преобразуем индекс в список строковых представлений дат
    forecast_dates_str = forecast_dates.strftime('%Y-%m-%d').tolist()

    # Передача данных в шаблон
    context = {
        'forecast_dates': forecast_dates_str,
        'forecast_values': forecast_values_rounded.tolist(),
    }
    print('context',context)
    
    return render(request, 'analytics/demand_forecast.html', context)

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
        df = df.set_index('dades_list')
        print('df',df)
        # Преобразование DataFrame в списки
        dades_list = df.index.tolist()

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
