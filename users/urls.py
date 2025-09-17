from django.urls import path
from .views import register, user_login, profile  # Добавьте profile
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),  # Добавьте эту строку
]