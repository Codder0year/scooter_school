# booking/forms.py
from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'trainer', 'course', 'metro', 'name', 'phone']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'trainer': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),  # заменили service на course
            'metro': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        trainer = cleaned_data.get('trainer')
        course = cleaned_data.get('course')

        if trainer and course:
            if not trainer.course.filter(id=course.id).exists():  # проверка на курсы
                self.add_error('course', 'Этот тренер не предоставляет выбранный курс')
        elif trainer and not course:
            self.add_error('course', 'Пожалуйста, выберите курс тренера')
        elif course and not trainer:
            self.add_error('trainer', 'Пожалуйста, выберите тренера для курса')
        else:
            self.add_error(None, 'Пожалуйста, выберите тренера и курс или курс и тренера')
