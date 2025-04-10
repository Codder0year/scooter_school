# Generated by Django 5.1.6 on 2025-03-29 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_trainers'),
        ('trainers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainer',
            name='courses',
            field=models.ManyToManyField(blank=True, related_name='trainers_set', to='courses.course'),
        ),
    ]
