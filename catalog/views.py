from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Category

def product_list(request):
    # Получаем все товары
    products = Product.objects.all()
    
    # Фильтрация по категориям
    category_filters = request.GET.getlist('category')
    if category_filters:
        products = products.filter(category__id__in=category_filters)
    
    # Фильтрация по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and min_price != '':
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price and max_price != '':
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Фильтрация по наличию
    in_stock = request.GET.get('in_stock')
    if in_stock:
        products = products.filter(in_stock=True)
    
    # Сортировка
    sort_by = request.GET.get('sort_by', 'created_at')
    if sort_by == 'price':
        products = products.order_by('price')
    elif sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'popularity':
        products = products.order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    # Получаем все категории для фильтров
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'current_filters': {
            'category': category_filters,
            'min_price': min_price or '',
            'max_price': max_price or '',
            'in_stock': bool(in_stock),
            'sort_by': sort_by,
        }
    }
    
    return render(request, 'catalog/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'catalog/product_detail.html', {'product': product})