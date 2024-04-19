from django_filters import FilterSet, DateFilter, ModelChoiceFilter, CharFilter, Filter
from django.db.models import Q
from .models import Item, Product
from warehouses.models import Stock
from django.forms import DateInput,Select,TextInput

class DateRangLteFilter(Filter):
    def filter(self, qs, value):
        if value:
            return qs.filter(Q(purchase_date__lte=value, sold=False) | Q(sales_date__lte=value, sold=True))
        return qs
    
class DateRangGetFilter(Filter):
    def filter(self, qs, value):
        if value:
            return qs.filter(Q(purchase_date__gte=value, sold=False) | Q(sales_date__gte=value, sold=True))
        return qs

class ItemFilter(FilterSet):
    purchase_date = DateFilter(
        label='Дата поступления:',
        field_name='purchase_date',
        lookup_expr='exact',
        widget=DateInput(attrs={'type': 'date','class': 'form-control',})
    )
    purchase_date__gte = DateFilter(
        label='Дата поступления от',
        field_name='purchase_date',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date','class': 'form-control',})
    )
    purchase_date__lte = DateFilter(
        label='Дата поступления до',
        field_name='purchase_date',
        lookup_expr='lte',
        widget=DateInput(attrs={'type': 'date','class': 'form-control',})
    )
    sales_date = DateFilter(
        label='Дата сбыта:',
        field_name='sales_date',
        lookup_expr='exact',
        widget=DateInput(attrs={'type': 'date','class': 'form-control',})
    )
    sales_date__gte = DateFilter(
        label='Дата сбыта от',
        field_name='sales_date',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date','class': 'form-control',})
    )
    sales_date= DateFilter(
        label='Дата сбыта до',
        field_name='sales_date',
        lookup_expr='lte',
        widget=DateInput(attrs={'type': 'date','class': 'form-control',})
    )
    date_range__lte = DateRangLteFilter(
        field_name='your_date_field', 
        label='Дата до:', 
        widget=DateInput(attrs={'type': 'date','class': 'form-control',}))
    date_range__gte = DateRangGetFilter(
        field_name='your_date_field', 
        label='Дата от:', 
        widget=DateInput(attrs={'type': 'date','class': 'form-control',}))
    
    stock = ModelChoiceFilter(
        queryset=Stock.objects.all(),  # Замените Stock.objects.all() на ваш запрос, если необходимо
        field_name='stock',  # Укажите поле внешнего ключа, по которому хотите фильтровать
        label='Склад', # Метка для фильтра
        widget= Select(attrs ={
                'class': 'form-select',
            }),
    )
    product = ModelChoiceFilter(
        queryset=Product.objects.all(),  # Замените Stock.objects.all() на ваш запрос, если необходимо
        field_name='product',  # Укажите поле внешнего ключа, по которому хотите фильтровать
        label='Продукт',  # Метка для фильтра
        widget= Select(attrs ={
                'class': 'form-select',
            }),
    )
    vendor_code = CharFilter(label='Артикул',
        field_name='product__vendor_code', 
        lookup_expr='icontains',
        widget= TextInput(attrs = {
                'class': 'form-control',
                'placeholder':"Артикул"
            })
    )
    

    