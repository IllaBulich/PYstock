from django.db import models


class Product(models.Model):

    name = models.CharField('Название',max_length = 50)
    description = models.TextField('Описание')
    vendor_code = models.CharField('Артикул', max_length = 50)
    quantity_rack = models.IntegerField('Количество на одином стилаже')
    

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/product/{self.id}'
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


