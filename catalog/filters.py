# catalog/filters.py
import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact')
    
    class Meta:
        model = Product
        fields = ['category']
    
    ORDER_CHOICES = [
        ('year', 'Году выпуска'),
        ('name', 'Названию'),
        ('price', 'Цене'),
    ]
    
    order = django_filters.OrderingFilter(
        choices=ORDER_CHOICES,
        fields={
            'year': 'year',
            'name': 'name',
            'price': 'price',
        }
    )