from django.db import models

CHOICES_DIRECTION = (
    ('trainer', 'Выбрать тренера'),
    ('service', 'Выбрать услугу'),
)


class Booking(models.Model):
    date = models.DateField(verbose_name="Дата тренировки")
    time = models.TimeField(verbose_name="Время тренировки")
    direction = models.CharField(max_length=20, choices=CHOICES_DIRECTION, verbose_name="Выбор направления")

    # Если выбран конкретный тренер, ссылаемся на модель из приложения trainers
    trainer = models.ForeignKey(
        'trainers.Trainer',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Тренер"
    )

    # Если выбрана услуга, ссылаемся на модель из приложения courses
    service = models.ForeignKey(
        'courses.Course',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Услуга"
    )

    metro = models.CharField(max_length=100, verbose_name="Станция метро")
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата записи")

    def __str__(self):
        return f"Запись {self.name} на {self.date} в {self.time}"
