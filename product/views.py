from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Item
from .forms import ProductForm, ItemForm
from django.views.generic import DetailView, DeleteView ,UpdateView
from django.http import JsonResponse
import json


def delete_item(request, item_id):
    # Получаем объект Item или возвращаем ошибку 404, если он не найден
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        quantity_to_delete = int(request.POST.get('quantityDelete'))
        if quantity_to_delete > item.quantity:
            # Если запрошенное количество для удаления больше, чем имеющееся количество, вы можете добавить обработку ошибки здесь
            pass
        else:
            item.quantity -= quantity_to_delete
            item.save()
            # Редирект на страницу, отображающую список Item или куда-либо еще по вашему усмотрению
            return redirect('warehouses/main')  # Не забудьте указать имя URL для страницы со списком Item

    # Если запрос не POST, возвращаем какую-то другую страницу, или можете передать данные для отображения формы удаления
    return redirect('warehouses/main')

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product/main')  # Предположим, что у вас есть URL с именем 'item_list' для списка товаров
    else:
        form = ItemForm()
    return render(request, 'product/add_item.html', {'form': form})



def salesItem(request):
    items = Item.objects.filter(available=True)
    if request.method == 'POST':
        try:
            # Парсим JSON из тела запроса
            data = json.loads(request.body)
            # Выводим полученные данные в консоль
            print("Received data in salesItem:", data)
            for item in data:
               
                print(Item.createSaleItem(item))
            # Возвращаем ответ об успешной обработке
            return redirect('warehouses/main')
        except json.JSONDecodeError:
            # Если возникла ошибка при разборе JSON, возвращаем сообщение об ошибке
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return render(request,'product/sales_item.html',{'items':items,})

    

class ProductUpdateView(UpdateView):
    model = Product
    template_name = "product/add.html"
    
    form_class = ProductForm

class ProductDeleteView(DeleteView):
    model = Product
    success_url = '/product'
    template_name = "product/delete.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/details_view.html"
    context_object_name = "product"

def main(request):
    product = Product.objects.all()
    return render(request,'product/main.html',{'product':product})

def add(request):
    error = ''
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('product/main')
        else:
            error = "неверные даные"

    form = ProductForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request,'product/add.html',data)