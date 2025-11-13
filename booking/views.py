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
        trainers = Trainer.objects.all()
        courses = Course.objects.all()

        return render(request, self.template_name, {
            'form': form,
            'trainers': trainers,
            'courses': courses
        })

    def post(self, request, *args, **kwargs):
        form = BookingForm(request.POST)
        trainers = Trainer.objects.all()
        courses = Course.objects.all()

        if form.is_valid():
            booking = form.save()

            # Отправка уведомления в Telegram
            success = self.send_telegram_notification(booking)

            if success:
                messages.success(request, "Спасибо за запись! Мы свяжемся с вами для подтверждения.")
            else:
                messages.warning(request, "Запись сохранена, но не удалось отправить уведомление. Мы свяжемся с вами.")

            return redirect('booking:booking_success')

        return render(request, self.template_name, {
            'form': form,
            'trainers': trainers,
            'courses': courses
        })

    def send_telegram_notification(self, booking):
        """Отправка уведомления в Telegram"""
        try:
            # Проверяем наличие настроек
            if not hasattr(settings, 'TELEGRAM_BOT_TOKEN') or not hasattr(settings, 'TELEGRAM_CHAT_ID'):
                print("TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не настроены")
                return False

            token = settings.TELEGRAM_BOT_TOKEN
            chat_id = settings.TELEGRAM_CHAT_ID

            # Формируем сообщение
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
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }

            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()

            print(f"Telegram уведомление отправлено успешно! Статус: {response.status_code}")
            return True

        except requests.exceptions.RequestException as e:
            print(f"Ошибка отправки Telegram уведомления: {e}")
            return False
        except Exception as e:
            print(f"Неожиданная ошибка при отправке в Telegram: {e}")
            return False


# Остальные функции остаются без изменений
def get_trainer_courses(request, trainer_id):
    try:
        trainer = Trainer.objects.get(id=trainer_id)
        courses = trainer.course.all()
        data = [{'id': course.id, 'name': course.title} for course in courses]
        return JsonResponse(data, safe=False)
    except Trainer.DoesNotExist:
        return JsonResponse([], safe=False)


def get_course_trainers(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        trainers = course.trainers_list.all()
        data = [{'id': trainer.id, 'name': trainer.name} for trainer in trainers]
        return JsonResponse(data, safe=False)
    except Course.DoesNotExist:
        return JsonResponse([], safe=False)


class BookingSuccessView(TemplateView):
    template_name = 'booking/success.html'