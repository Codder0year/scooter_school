from django.db import models
from courses.models import Course  # Предполагается, что модель Course уже существует


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='trainers_photos/')
    course = models.ManyToManyField('courses.Course', related_name='trainers_list',
                                    blank=True)  # Изменено на 'trainers_list'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Добавляем курсы к тренеру
        for course in self.course.all():
            if self not in course.trainers.all():
                course.trainers.add(self)
                course.save()

    def __str__(self):
        return self.name
