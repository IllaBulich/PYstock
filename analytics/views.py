from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from product.models import Item
from django.db.models import  F, ExpressionWrapper, FloatField
import json
from datetime import datetime, date


def view_func(request):
   
    items = (
        Item.objects.filter(sold=False)
        .values('purchase_date')
        .annotate(received=ExpressionWrapper(F('quantity') * F('purchase_price'), output_field=FloatField()))
        .annotate(remainder = ExpressionWrapper(  (F('quantity')-F('soldQuantity'))* F('purchase_price'), output_field=FloatField()) )
        .order_by('purchase_date')
        )
    
    print('items =',items)

    dades_list = list()
    all_price_dates_dict = dict()
    all_remainder_dict = dict()

    for item in items:
        if not item['purchase_date'] in dades_list:
            dades_list.append(item['purchase_date'])
        
        if item['purchase_date'] in all_price_dates_dict:
            all_price_dates_dict[item['purchase_date']] += item['received']
        else:
            all_price_dates_dict[item['purchase_date']] = item['received']

        if item['purchase_date'] in all_remainder_dict:
            all_remainder_dict[item['purchase_date']] += item['remainder']
        else:
            all_remainder_dict[item['purchase_date']] = item['remainder']


    all_price_dates_list = list()
    all_remainder_list = list()
    for dates in dades_list:
        if dates in all_price_dates_dict:
            all_price_dates_list.append(all_price_dates_dict[dates])
        else:
            all_price_dates_list.append(0)

        if dates in all_remainder_dict:
            all_remainder_list.append(all_remainder_dict[dates])
        else:
            all_remainder_list.append(0)

   
    charts_data = dict()
    charts_data['line_chart'] = dict()
    charts_data['line_chart']['dades_list'] = dades_list
    charts_data['line_chart']['series'] = [
        {'name':'Поступления на суму', 'data': all_price_dates_list},
        {'name':'Осталось на суму', 'data': all_remainder_list},
        ]

    def custom_serializer(obj):
        if isinstance(obj, (datetime,date)):
            serial = obj.isoformat()
            return serial

    json_charts_data = json.dumps(charts_data,  default=custom_serializer)

    return render(request, 'analytics/main.html', {'charts_data': json_charts_data})