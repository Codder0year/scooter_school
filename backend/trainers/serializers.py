from rest_framework import serializers
from .models import Trainer
from django.apps import apps


class TrainerSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = '__all__'
        ref_name = 'TrainersTrainerSerializer'

    def get_courses(self, obj):
        Course = apps.get_model('courses', 'Course')
        from backend.courses.serializers import CourseSerializer
        courses = Course.objects.filter(trainers_list=obj)
        return CourseSerializer(courses, many=True).data
