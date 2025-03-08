from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Ваше имя')
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Сообщение')  # уменьшили высоту
    phone = forms.CharField(max_length=20, label='Ваш телефон')