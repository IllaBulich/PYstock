from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from .filters import ItemFilter
from .models import  Item, SalesItem
from .forms import  ItemForm, QRCodeUploadForm
from django.views.generic import DetailView,  UpdateView,  CreateView
from django.http import JsonResponse
import json
import qrcode
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from PIL import Image
from pyzbar.pyzbar import decode
from django.core.paginator import Paginator

def upload_qr_code(request):
    if request.method == 'POST':
        form = QRCodeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Получаем изображение из формы
            image = form.cleaned_data['image']
            
            # Считываем QR-коды на изображении
            decoded_objects = decode(Image.open(image))

            # Получаем данные из QR-кодов
            qr_data = [obj.data.decode('utf-8') for obj in decoded_objects]

            # Получаем последний элемент списка
            last_url = qr_data[0]

            # Разбиваем URL-адрес по символу '/' и получаем последний элемент
            last_number = last_url.split('/')[-1]

            # Преобразуем последний номер в целое число
            last_number_int = int(last_number)
            try:
                item = get_object_or_404(Item, pk=last_number_int)
                # Отобразить данные QR-кода на странице
                return render(request, 'item/qr_code_result.html', {'item': item})
            except:
                return render(request, 'item/upload_qr.html', {'form': form, 'error_message': 'Объект с таким ID не найден.'})
        
            
    else:
        form = QRCodeUploadForm()
    return render(request, 'item/upload_qr.html', {'form': form})

def generate_qr_code(request, item_id):
    # # Получаем объект модели Item
    # item = get_object_or_404(Item, pk=item_id)

    # Создаем URL-адрес страницы деталей объекта модели Item
    item_detail_url = request.build_absolute_uri(reverse('item:item_detail', kwargs={'pk': item_id}))

    # Создание объекта QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Добавление URL-адреса в объект QRCode
    qr.add_data(item_detail_url)
    qr.make(fit=True)

    # Создание изображения QR-кода
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Создание HTTP-ответа с изображением QR-кода
    response = HttpResponse(content_type="image/png")
    qr_img.save(response, "PNG")
    return response
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

class SalesItemDetailView(LoginRequiredMixin,DetailView):
    model = SalesItem
    template_name = "item/details_sales_item_view.html"
    context_object_name = "item"

class ItemUpdateView(LoginRequiredMixin,UpdateView):
    model = Item
    template_name = "item/update_item.html"
    form_class = ItemForm
   

class ItemListView(LoginRequiredMixin,FilterView):
    model = Item
    filterset_class = ItemFilter
    template_name = 'item/sales_item.html'
    paginate_by = 3 
    context_object_name = 'item'

    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(available=True)
       
        return queryset
    

    def post(self, request):
        try:
            # Парсим JSON из тела запроса
            data = json.loads(request.body)
            # Выводим полученные данные в консоль
            print("Received data in salesItem:", data)
            for item_data in data:
               
                # Вместо вызова Item.createSaleItem(item_data) предполагается, что
                # у вас есть метод createSaleItem в модели Item или менеджере модели
                print(Item.createSaleItem(item_data,self.request.user))
            # Возвращаем ответ об успешной обработке
            return redirect('warehouses:main')
        except json.JSONDecodeError:
            # Если возникла ошибка при разборе JSON, возвращаем сообщение об ошибке
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
