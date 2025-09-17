# main/admin.py
from django.contrib import admin
from .models import Slide

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active']
    list_editable = ['is_active']