from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from .models import Item, Product
from warehouses.models import Stock
from django.forms import DateInput,Select

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


    class Meta:
        model = Item
        fields = {
            
            'purchase_date': ['exact', 'gte', 'lte'],
            # Добавьте остальные поля, по которым хотите фильтровать
        }
        