
from django.forms import DateInput, DateField, Form

class DateRangeForm(Form):
    date_from = DateField(label='Дата от',
                                required=False,
                                widget=DateInput(attrs={'type': 'date','class': 'form-control',}))
    date_to = DateField(label='Дата до', 
                              required=False,
                              widget=DateInput(attrs={'type': 'date','class': 'form-control',}))
   