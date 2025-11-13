from django.core.exceptions import ValidationError
from django.db import models


class Booking(models.Model):
    date = models.DateField(verbose_name="Дата тренировки")
    time = models.TimeField(verbose_name="Время тренировки")

    # Убрали direction - теперь определяется логикой выбора

    trainer = models.ForeignKey(
        'trainers.Trainer',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Тренер"
    )

    course = models.ForeignKey(
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

    def clean(self):
        """Проверка, что выбран либо тренер+курс, либо курс+тренер"""
        if not self.trainer and not self.course:
            raise ValidationError("Должен быть выбран либо тренер, либо курс")

        if self.trainer and self.course:
            # Проверяем, что тренер ведет этот курс
            if not self.trainer.course.filter(id=self.course.id).exists():
                raise ValidationError("Этот тренер не ведет выбранный курс")