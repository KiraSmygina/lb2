# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Пароль', 
        widget=forms.PasswordInput, 
        min_length=6, 
        help_text="Минимум 6 символов"
    )
    password2 = forms.CharField(
        label='Подтверждение пароля', 
        widget=forms.PasswordInput
    )
    rules = forms.BooleanField(
        label='Я согласен с правилами регистрации', 
        required=True
    )
    
    class Meta:
        model = CustomUser
        fields = ['name', 'surname', 'patronymic', 'username', 'email', 'password1', 'password2', 'rules']
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z0-9\-]+$', username):
            raise forms.ValidationError('Разрешены только латиница, цифры и тире.')
        return username