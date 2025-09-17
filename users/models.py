# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import re
from django.core.exceptions import ValidationError

def validate_cyrillic(value):
    if not re.match(r'^[А-Яа-яёЁ\s\-]+$', value):
        raise ValidationError('Разрешены только кириллица, пробелы и тире.')

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, validators=[validate_cyrillic], verbose_name="Имя")
    surname = models.CharField(max_length=100, validators=[validate_cyrillic], verbose_name="Фамилия")
    patronymic = models.CharField(max_length=100, blank=True, validators=[validate_cyrillic], verbose_name="Отчество")
    email = models.EmailField(unique=True, verbose_name="Email")
    
    # Добавляем уникальные related_name для избежания конфликтов
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",  # Уникальное имя
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",  # Уникальное имя
        related_query_name="customuser",
    )
    
    def __str__(self):
        return f"{self.surname} {self.name}"
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"