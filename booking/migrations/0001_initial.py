# Generated by Django 5.1.6 on 2025-03-28 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0005_course_suitable_for'),
        ('trainers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата тренировки')),
                ('time', models.TimeField(verbose_name='Время тренировки')),
                ('direction', models.CharField(choices=[('trainer', 'Выбрать тренера'), ('service', 'Выбрать услугу')], max_length=20, verbose_name='Выбор направления')),
                ('metro', models.CharField(max_length=100, verbose_name='Станция метро')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.course', verbose_name='Услуга')),
                ('trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='trainers.trainer', verbose_name='Тренер')),
            ],
        ),
    ]
