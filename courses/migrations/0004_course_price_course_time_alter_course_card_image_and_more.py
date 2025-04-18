# Generated by Django 5.1.6 on 2025-03-03 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_remove_course_image_course_card_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Цена'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='time',
            field=models.CharField(default=0, max_length=100, verbose_name='Время'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='card_image',
            field=models.ImageField(blank=True, null=True, upload_to='courses/images/', verbose_name='Картинка карточки'),
        ),
        migrations.AlterField(
            model_name='course',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='course',
            name='detail_image',
            field=models.ImageField(blank=True, null=True, upload_to='courses/detail_images/', verbose_name='Картинка для детали'),
        ),
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название курса'),
        ),
    ]
