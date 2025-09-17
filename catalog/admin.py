# catalog/admin.py
from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'in_stock', 'created_at']
    list_filter = ['category', 'in_stock', 'created_at']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']