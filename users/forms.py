# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import CustomUser
import re

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Пароль', 
        widget=forms.PasswordInput, 
        min_length=6, 
        help_text="Минимум 6 символов",
        error_messages={
            'required': 'Введите пароль',
            'min_length': 'Пароль должен содержать не менее 6 символов',
        }
    )
    password2 = forms.CharField(
        label='Подтверждение пароля', 
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Повторите пароль',
        }
    )
    rules = forms.BooleanField(
        label='Я согласен с правилами регистрации', 
        required=True
    )
    
    class Meta:
        model = CustomUser
        fields = ['name', 'surname', 'patronymic', 'username', 'email', 'password1', 'password2', 'rules']
        help_texts = {
            'username': '',
        }
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z0-9\-]+$', username):
            raise forms.ValidationError('Разрешены только латиница, цифры и тире.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Введите email')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Пароли не совпадают')
            if len(password2) < 6:
                raise forms.ValidationError('Пароль должен содержать не менее 6 символов')
        try:
            validate_password(password2, self.instance)
        except DjangoValidationError as e:
                messages = []
                for m in e.messages:
                    if m.startswith('This password is too short.'):
                        messages.append('Пароль слишком короткий. Минимальная длина 6 символов.')
                    else:
                        messages.append(m)
                raise forms.ValidationError(messages)
        return password2


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['username'].help_text = ''
        # Переводим ключевые сообщения ошибок
        self.error_messages.update({
            'invalid_login': 'Пожалуйста, введите корректные логин и пароль. Учетные данные не совпадают.',
            'inactive': 'Учетная запись неактивна.'
        })