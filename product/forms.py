from .models import Product
from django.forms import ModelForm, TextInput,  NumberInput,Textarea 


   

class ProductForm(ModelForm):
     class Meta:
        model = Product
        fields = ['name', 'description', 'vendor_code', 'quantity_rack']

        widgets = {
            'name': TextInput(attrs = {
                'class': 'form-control',
                'placeholder':"Название"
            }),
            'description': Textarea(attrs = {
                'class': 'form-control',
                'placeholder':"Описание"
            }),
            'vendor_code': TextInput(attrs = {
                'class': 'form-control',
                'placeholder':"Артикул"
            }),
         
            'quantity_rack': NumberInput(attrs ={
                'class': 'form-control',
                'placeholder':"Количество на одином стилаже",
                'min': 0,
            }),
            # 'occupancy_status': NumberInput(attrs ={
            #     'class': 'form-control',
            #     'placeholder':"Количесто стилажей",
            #     'min': 0,
            #     'step': 0.01
            # }),

        }