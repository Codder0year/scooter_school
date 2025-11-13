from django.db import models

# Create your models here.
from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    video = models.FileField(upload_to='news_videos/', blank=True, null=True)

    def __str__(self):
        return self.title