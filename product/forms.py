from .models import Product, Item
from django.forms import ModelForm, TextInput, Select, DateInput, NumberInput,Textarea , Form , IntegerField, DecimalField

class ItemForm(ModelForm):
    # purchase_date = DateField(label='Дата поступления', widget=DateInput(attrs={'class': 'vDateField', 'size': '10', 'required': True}))
    class Meta:
        model = Item
        fields = ['product', 'stock','quantity', 'purchase_price', 'purchase_date']
        widgets = {
            'product': Select(attrs ={
                'class': 'form-select',
                
            }),
            'stock': Select(attrs ={
                'class': 'form-select',
                
            }),
            'quantity': NumberInput(attrs ={
                'class': 'form-control',
                'placeholder':"Количество ",
                'min': 0,
            }),
            'purchase_price': NumberInput(attrs ={
                'class': 'form-control',
                'placeholder':"Стоймость",
                'min': 0,
                'step': 0.01
            }),
            'purchase_date': DateInput(attrs ={
                'class': 'form-control',
                'type':"date",
                'placeholder':"Дата",
                
            }),
            # 'purchase_date': SelectDateWidget(
            #     years=range(1940, 2024),
            # ),

        }



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