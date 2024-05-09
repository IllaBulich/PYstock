
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from .forms import ProductForm
from django.views.generic import DetailView, DeleteView, UpdateView,  ListView, CreateView




class ProductUpdateView(LoginRequiredMixin,UpdateView):
    model = Product
    template_name = "product/add.html"
    form_class = ProductForm

class ProductDeleteView(LoginRequiredMixin,DeleteView):
    model = Product
    success_url = '/product'
    template_name = "product/delete.html"


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product/details_view.html"
    context_object_name = "product"


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "product/main.html"
    context_object_name = "product"
    paginate_by = 10  



class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/add.html'

    def get_success_url(self):
        # Получаем параметр 'next' из запроса
        next_url = self.request.GET.get('next')

        # Если параметр 'next' существует, возвращаем его значение
        if next_url:
            return next_url
        
        # Если параметр 'next' отсутствует, возвращаем URL по умолчанию
        return reverse('product/main')
