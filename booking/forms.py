# booking/forms.py
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'trainer', 'course', 'metro', 'name', 'phone']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': '2024-01-01'  # Минимальная дата
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'min': '08:00',  # Минимальное время
                'max': '22:00'   # Максимальное время
            }),
            'trainer': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'metro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Начните вводить станцию метро...'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (XXX) XXX-XX-XX'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Простая валидация телефона
        if phone and not any(char.isdigit() for char in phone):
            raise forms.ValidationError("Введите корректный номер телефона")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        trainer = cleaned_data.get('trainer')
        course = cleaned_data.get('course')

        # Проверяем, что выбран либо тренер, либо курс
        if not trainer and not course:
            raise forms.ValidationError("Пожалуйста, выберите тренера или курс")

        # Проверяем совместимость тренера и курса
        if trainer and course and not trainer.course.filter(id=course.id).exists():
            raise forms.ValidationError("Этот тренер не ведет выбранный курс")