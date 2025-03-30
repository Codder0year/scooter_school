from django.db import models
from courses.models import Course  # Предполагается, что модель Course уже существует


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='trainers_photos/')
    courses = models.ManyToManyField('courses.Course', related_name='trainers_list', blank=True)

    def __str__(self):
        return self.name