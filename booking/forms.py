from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'direction', 'trainer', 'service', 'metro', 'name', 'phone']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'direction': forms.RadioSelect(),
            'trainer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Выберите тренера'}),
            'service': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Выберите услугу'}),
            'metro': forms.TextInput(attrs={
                'class': 'form-control autocomplete',
                'placeholder': 'Начните вводить название станции'
            }),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш телефон'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        direction = cleaned_data.get('direction')
        trainer = cleaned_data.get('trainer')
        service = cleaned_data.get('service')

        if direction == 'trainer' and not trainer:
            self.add_error('trainer', 'Укажите, пожалуйста, тренера.')
        elif direction == 'service' and not service:
            self.add_error('service', 'Укажите, пожалуйста, услугу.')
        return cleaned_data
