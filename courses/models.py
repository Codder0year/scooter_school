from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание')
    card_image = models.ImageField(upload_to='courses/images/', blank=True, null=True, verbose_name='Картинка карточки')
    detail_image = models.ImageField(upload_to='courses/detail_images/', blank=True, null=True, verbose_name='Картинка для детали')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time = models.CharField(max_length=100, verbose_name='Время')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    suitable_for = models.CharField(max_length=200, blank=True, null=True, verbose_name='Для кого подходит')
    trainers = models.ManyToManyField('trainers.Trainer', related_name='courses_list', blank=True)

    def __str__(self):
        return self.title
