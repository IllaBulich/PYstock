
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Stock
from .forms import StockForm
from django.views.generic import DetailView, DeleteView ,UpdateView, ListView, CreateView



class StockUpdateView(LoginRequiredMixin,UpdateView):
    model = Stock
    template_name = "warehouses/add.html"
    
    form_class = StockForm

class StockDeleteView(LoginRequiredMixin,DeleteView):
    model = Stock
    success_url = '/warehouses'
    template_name = "warehouses/delete.html"


class StockDetailView(DetailView):
    model = Stock
    template_name = "warehouses/details_view.html"
    context_object_name = "stock"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock = self.get_object()
        items = stock.item_set.filter(available=True)
        context['items'] = items
        return context


class StockListView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = "warehouses/main.html"
    context_object_name = "stock"


class AddStockView(LoginRequiredMixin, CreateView):
    model = Stock
    form_class = StockForm
    template_name = 'warehouses/add.html'
