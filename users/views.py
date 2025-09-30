from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, CustomAuthenticationForm
from .models import CustomUser
from orders.models import Order
from django.http import JsonResponse
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({ 'ok': True, 'redirect': reverse('home') })
            return redirect('home')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({ 'ok': False, 'errors': form.errors }, status=400)
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            try:
                cu = CustomUser.objects.get(username=username)
                if cu.check_password(password):
                    cu.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, cu)
                    return redirect('home')
            except CustomUser.DoesNotExist:
                pass
        else:
            login(request, user)
            return redirect('home')
    return render(request, 'users/login.html', {'form': form})

# Добавьте это представление
@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/profile.html', { 'orders': orders })