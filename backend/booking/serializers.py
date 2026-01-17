from rest_framework import serializers
from .models import Booking
from courses.models import Course
from trainers.models import Trainer


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = '__all__'
        ref_name = 'BookingTrainerSerializer'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        ref_name = 'BookingCourseSerializer'


class BookingSerializer(serializers.ModelSerializer):
    trainer = TrainerSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    trainer_id = serializers.PrimaryKeyRelatedField(
        queryset=Trainer.objects.all(), source='trainer', write_only=True, allow_null=True, required=False
    )
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = Booking
        fields = [
            'id', 'date', 'time', 'trainer', 'course', 'metro', 'name', 'phone', 'created_at',
            'trainer_id', 'course_id'
        ]

    def validate(self, data):
        trainer = data.get('trainer')
        course = data.get('course')

        if not trainer and not course:
            raise serializers.ValidationError("Должен быть выбран либо тренер, либо курс")

        if trainer and course and not trainer.course.filter(id=course.id).exists():
            raise serializers.ValidationError("Этот тренер не ведет выбранный курс")

        return data
