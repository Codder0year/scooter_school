from rest_framework import serializers
from courses.models import Course
from django.apps import apps  # <- Добавляем ленивый импорт


class CourseSerializer(serializers.ModelSerializer):
    trainers = serializers.SerializerMethodField()  # <- Динамически загружаем тренеров

    class Meta:
        model = Course
        fields = '__all__'

    def get_trainers(self, obj):
        Trainer = apps.get_model('trainers', 'Trainer')  # <- Ленивый импорт
        from trainers.serializers import TrainerSerializer  # <- Импорт внутри функции
        trainers = Trainer.objects.filter(courses_list=obj)
        return TrainerSerializer(trainers, many=True).data
