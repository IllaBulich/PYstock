from .models import Stock
from django.forms import ModelForm, TextInput, NumberInput

class StockForm(ModelForm):
     class Meta:
        model = Stock
        fields = ['title', 'city', 'street', 'address', 'number_racks']

        widgets = {
            'title': TextInput(attrs = {
                'class': 'form-control',
                'placeholder':"Название склада"
            }),
            'city': TextInput(attrs = {
                'class': 'form-control',
                'placeholder':"Название города"
            }),
            'street': TextInput(attrs = {
                'class': 'form-control',
                'placeholder':"Название улицы"
            }),
            'address': TextInput(attrs = {
                'class': 'form-control',
                'placeholder':"Номер дома"
            }),
            'number_racks': NumberInput(attrs ={
                'class': 'form-control',
                'placeholder':"Количесто стилажей",
                'min': 0,
            }),
            # 'occupancy_status': NumberInput(attrs ={
            #     'class': 'form-control',
            #     'placeholder':"Количесто стилажей",
            #     'min': 0,
            #     'step': 0.01
            # }),

        }