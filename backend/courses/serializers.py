from rest_framework import serializers
from .models import Course
from django.apps import apps


class CourseSerializer(serializers.ModelSerializer):
    trainers = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        ref_name = 'CoursesCourseSerializer'  # уникальное имя

    def get_trainers(self, obj):
        Trainer = apps.get_model('trainers', 'Trainer')
        from backend.trainers.serializers import TrainerSerializer
        trainers = Trainer.objects.filter(courses_list=obj)
        return TrainerSerializer(trainers, many=True).data
