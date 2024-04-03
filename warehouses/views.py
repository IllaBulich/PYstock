from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Stock
from .forms import StockForm
from django.views.generic import DetailView, DeleteView ,UpdateView



class StockUpdateView(LoginRequiredMixin,UpdateView):
    model = Stock
    template_name = "warehouses/add.html"
    
    form_class = StockForm

class StockDeleteView(LoginRequiredMixin,DeleteView):
    model = Stock
    success_url = '/warehouses'
    template_name = "warehouses/delete.html"


# class StockDetailView(DetailView):
#     model = Stock
#     template_name = "warehouses/details_view.html"
#     context_object_name = "stock"

@login_required
def stock_detail(request, id):
    stock = get_object_or_404(Stock, id=id)
    items = stock.item_set.filter(available=True)
    return render(request,
                  'warehouses/details_view.html',
                  {'stock': stock, 
                   'items': items})
@login_required
def main(request):
    stock = Stock.objects.all()
    for el in stock:
        lol = el.calculation_occupancy_status()
        print("el =",lol)
    return render(request,'warehouses/main.html',{'stock':stock})

@login_required
def add(request):
    error = ''
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.ooccupancy_status = 0
            form.save()
            return redirect('warehouses/main')
        else:
            error = "неверные даные"

    form = StockForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request,'warehouses/add.html',data)