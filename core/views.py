from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from courses.models import Course
from .models import News


def home(request):
    # Получаем три конкретных курса
    courses = Course.objects.filter(title__in=['Базовый курс', 'Продвинутый курс',
                                               'Индивидуальное занятие с Егором: Мастерство'
                                               ' и уверенность на самокате']).order_by('title')[:3]
    return render(request, 'home.html', {'courses': courses})


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list'] = News.objects.order_by('-date_posted')
        return context


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Обработка данных формы
            return render(request, 'thank_you.html')  # Страница благодарности
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def about_view(request):
    news_list = News.objects.order_by('-date_posted')  # последние новости сверху
    return render(request, 'core/about.html', {'news_list': news_list})
