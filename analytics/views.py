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
        print('queryset', queryset)
        items1 = (
            queryset.filter(sold=False)
            .values('purchase_date')
            .annotate(received=ExpressionWrapper(F('quantity') * F('purchase_price'), output_field=FloatField()))
            .annotate(remainder=ExpressionWrapper((F('quantity') - F('soldQuantity')) * F('purchase_price'), output_field=FloatField()))
            .order_by('purchase_date')
        )

        cost_chart = line_chart(items1)
        charts_data = {'cost_chart': cost_chart}

        items2 = (
            queryset.filter(sold=False)
            .values('purchase_date')
            .annotate(received=F('quantity'))
            .annotate(remainder=F('quantity') - F('soldQuantity'))
            .order_by('purchase_date')
        )

        quantity_chart = line_chart(items2)
        charts_data['quantity_chart'] = quantity_chart

        def custom_serializer(obj):
            if isinstance(obj, (datetime, date)):
                serial = obj.isoformat()
                return serial

        json_charts_data = json.dumps(charts_data, default=custom_serializer)

        context['charts_data'] = json_charts_data
        return context



def view_func(request):
 
    items1 = (
        Item.objects.filter(sold=False)
        .values('purchase_date')
        .annotate(received=ExpressionWrapper(F('quantity') * F('purchase_price'), output_field=FloatField()))
        .annotate(remainder = ExpressionWrapper(  (F('quantity')-F('soldQuantity'))* F('purchase_price'), output_field=FloatField()) )
        .order_by('purchase_date')
        )

    cost_chart = line_chart(items1)
    charts_data = dict()
    charts_data['cost_chart'] = cost_chart

    items2 = (
        Item.objects.filter(sold=False)
        .values('purchase_date')
        .annotate(received=F('quantity') )
        .annotate(remainder =  F('quantity')-F('soldQuantity') )
        .order_by('purchase_date')
        )
   

    quantity_chart = line_chart(items2)
   
    charts_data['quantity_chart'] = quantity_chart

    def custom_serializer(obj):
        if isinstance(obj, (datetime,date)):
            serial = obj.isoformat()
            return serial

    json_charts_data = json.dumps(charts_data,  default=custom_serializer)

    print('charts_data= ',charts_data)

    return render(request, 'analytics/main.html', {'charts_data': json_charts_data})


def line_chart(model_list):
    dades_list = list()
    all_received_dict = dict()
    all_remainder_dict = dict()

    for model in model_list:
        if not model['purchase_date'] in dades_list:
            dades_list.append(model['purchase_date'])
        
        if model['purchase_date'] in all_received_dict:
            all_received_dict[model['purchase_date']] += model['received']
        else:
            all_received_dict[model['purchase_date']] = model['received']

        if model['purchase_date'] in all_remainder_dict:
            all_remainder_dict[model['purchase_date']] += model['remainder']
        else:
            all_remainder_dict[model['purchase_date']] = model['remainder']


    all_received_list = list()
    all_remainder_list = list()
    for dates in dades_list:
        if dates in all_received_dict:
            all_received_list.append(all_received_dict[dates])
        else:
            all_received_list.append(0)

        if dates in all_remainder_dict:
            all_remainder_list.append(all_remainder_dict[dates])
        else:
            all_remainder_list.append(0)


    charts_data = dict()
    charts_data['dades_list'] = dades_list
    charts_data['series'] = [
        {'name':'Поступления', 'data': all_received_list},
        {'name':'Осталось', 'data': all_remainder_list},
        ]
    
    return charts_data