from django.shortcuts import render
from .models import Slide

def home(request):
    return render(request, 'main/index.html')

def contacts(request):
    return render(request, 'main/contacts.html')