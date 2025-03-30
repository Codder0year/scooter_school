import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.views.generic import TemplateView

from courses.models import Course
from trainers.models import Trainer
from .forms import BookingForm


class BookingCreateView(View):
    template_name = 'booking/booking_form.html'

    def get(self, request, *args, **kwargs):
        form = BookingForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # Отправка уведомления в Telegram
            self.send_telegram_notification(booking)

            messages.success(request, "Спасибо за обращение, ожидайте звонка!")  # Это сообщение
            return redirect('booking:booking_success')  # Можно редиректить на страницу успеха
        return render(request, self.template_name, {'form': form})

    def send_telegram_notification(self, booking):
        token = settings.TELEGRAM_BOT_TOKEN  # Добавьте в settings.py
        chat_id = settings.TELEGRAM_CHAT_ID  # Добавьте в settings.py
        message = (
            f"Новая запись:\n"
            f"Дата: {booking.date}\n"
            f"Время: {booking.time}\n"
            f"Направление: {booking.get_direction_display()}\n"
            f"Тренер: {booking.trainer or 'N/A'}\n"
            f"Услуга: {booking.course or 'N/A'}\n"
            f"Метро: {booking.metro}\n"
            f"Имя: {booking.name}\n"
            f"Телефон: {booking.phone}"
        )
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
        }
        try:
            requests.post(url, data=payload)
        except Exception as e:
            # Логирование ошибки отправки уведомления
            print(f"Ошибка отправки Telegram уведомления: {e}")


def get_trainer_courses(request, trainer_id):
    try:
        trainer = Trainer.objects.get(id=trainer_id)
        courses = trainer.courses.all()  # заменили services на courses
        data = [{'id': c.id, 'name': c.title} for c in courses]
        return JsonResponse(data, safe=False)
    except Trainer.DoesNotExist:
        return JsonResponse([], safe=False)


def get_course_trainers(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        trainers = course.trainers.all()  # заменили trainers на courses
        data = [{'id': t.id, 'name': t.name} for t in trainers]
        return JsonResponse(data, safe=False)
    except Course.DoesNotExist:
        return JsonResponse([], safe=False)


class BookingSuccessView(TemplateView):
    template_name = 'booking/success.html'
