from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
import requests
from .models import Booking
from courses.models import Course
from trainers.models import Trainer
from .serializers import BookingSerializer, TrainerSerializer, CourseSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('-created_at')
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        self.send_telegram_notification(booking)
        return Response(serializer.data)

    def send_telegram_notification(self, booking):
        try:
            token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
            chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)
            if not token or not chat_id:
                return False

            message = (
                f"🚴‍♂️ *НОВАЯ ЗАПИСЬ НА ТРЕНИРОВКУ*\n\n"
                f"📅 *Дата:* {booking.date}\n"
                f"⏰ *Время:* {booking.time}\n"
                f"👨‍🏫 *Тренер:* {booking.trainer.name if booking.trainer else 'Не указан'}\n"
                f"📚 *Курс:* {booking.course.title if booking.course else 'Не указан'}\n"
                f"📍 *Метро:* {booking.metro}\n"
                f"👤 *Имя:* {booking.name}\n"
                f"📞 *Телефон:* {booking.phone}\n"
                f"🕒 *Запись создана:* {booking.created_at.strftime('%d.%m.%Y %H:%M')}"
            )

            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, data={'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}, timeout=10)
            return True
        except:
            return False

    @action(detail=False, methods=['get'], url_path='trainer-courses/(?P<trainer_id>[^/.]+)')
    def trainer_courses(self, request, trainer_id=None):
        try:
            trainer = Trainer.objects.get(id=trainer_id)
            serializer = CourseSerializer(trainer.course.all(), many=True)
            return Response(serializer.data)
        except Trainer.DoesNotExist:
            return Response([], status=404)

    @action(detail=False, methods=['get'], url_path='course-trainers/(?P<course_id>[^/.]+)')
    def course_trainers(self, request, course_id=None):
        try:
            course = Course.objects.get(id=course_id)
            serializer = TrainerSerializer(course.trainers_list.all(), many=True)
            return Response(serializer.data)
        except Course.DoesNotExist:
            return Response([], status=404)
