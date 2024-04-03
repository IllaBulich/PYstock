from django.db import models

class Stock(models.Model):

    title = models.CharField('Название',max_length = 50)
    city = models.CharField('Город', max_length = 50)
    street = models.CharField('Улица', max_length = 50)
    address = models.CharField('Адрес', max_length = 50)
    number_racks = models.IntegerField('Количество стиложей')
    occupancy_status = models.FloatField('Заполниность стиложей',default=0)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/warehouses/{self.id}'
    
    def calculation_occupancy_status(self):
        self.occupancy_status = sum(item.calculation_quantity_rack() for item in self.item_set.filter(available=True))
        self.save()
        print('occupancy_status =',self.occupancy_status)
        return self.occupancy_status

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"