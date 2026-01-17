from django.db import models


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='trainers_photos/')
    course = models.ManyToManyField('courses.Course', related_name='trainers_list', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for course in self.course.all():
            if self not in course.trainers.all():
                course.trainers.add(self)
                course.save()

    def __str__(self):
        return self.name
