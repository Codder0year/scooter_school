from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from courses.models import Course


def home(request):
    # Получаем три конкретных курса
    courses = Course.objects.filter(title__in=['Базовый курс', 'Продвинутый курс',
                                               'Индивидуальное занятие с Егором: Мастерство'
                                               ' и уверенность на самокате']).order_by('title')[:3]
    return render(request, 'home.html', {'courses': courses})


class AboutView(TemplateView):
    template_name = 'core/about.html'


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Обработка данных формы
            return render(request, 'thank_you.html')  # Страница благодарности
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})