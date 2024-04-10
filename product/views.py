from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from .filters import ItemFilter
from .models import Product,Item
from .forms import ProductForm, ItemForm
from django.views.generic import DetailView, DeleteView, UpdateView,  ListView, CreateView
from django.http import JsonResponse
import json

# 
class AddItemView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'item/add_item.html'

    def form_valid(self, form):
        form.instance.responsible = self.request.user
        new_item = form.save(commit=False)
        if (new_item.stock.calculation_occupancy_status() +
                new_item.calculation_quantity_rack() > new_item.stock.number_racks):
            form.add_error(None, "Ошибка: Предельное количество стеллажей превышено")
            return self.form_invalid(form)
        else:
            new_item.save()
            new_item.stock.calculation_occupancy_status()
            return super().form_valid(form)
        


class ItemDetailView(LoginRequiredMixin,DetailView):
    model = Item
    template_name = "item/details_item_view.html"
    context_object_name = "item"

class ItemUpdateView(LoginRequiredMixin,UpdateView):
    model = Item
    template_name = "item/update_item.html"
    form_class = ItemForm
   

class ItemListView(LoginRequiredMixin,FilterView):
    model = Item
    filterset_class = ItemFilter
    template_name = 'item/sales_item.html'


    def get_queryset(self):
        queryset = super().get_queryset()
        # Получаем отфильтрованные результаты с помощью фильтра Django
        filtered_queryset = self.filterset_class(self.request.GET, queryset=queryset).qs
        # Возвращаем только элементы, у которых available=True
        return filtered_queryset.filter(available=True)
    

    def post(self, request):
        try:
            # Парсим JSON из тела запроса
            data = json.loads(request.body)
            # Выводим полученные данные в консоль
            print("Received data in salesItem:", data)
            for item_data in data:
                # Вместо вызова Item.createSaleItem(item_data) предполагается, что
                # у вас есть метод createSaleItem в модели Item или менеджере модели
                print(Item.createSaleItem(item_data))
            # Возвращаем ответ об успешной обработке
            return redirect('warehouses/main')
        except json.JSONDecodeError:
            # Если возникла ошибка при разборе JSON, возвращаем сообщение об ошибке
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)




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



class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/add.html'
