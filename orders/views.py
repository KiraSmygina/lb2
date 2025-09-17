# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Product
from django.contrib import messages

@login_required
def cart_view(request):
    # Получаем корзину пользователя или создаем новую, если ее нет
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    context = {
        'cart': cart,
        'cart_items': cart.items.all()
    }
    return render(request, 'orders/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Проверяем, есть ли товар уже в корзине
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'Товар "{product.name}" добавлен в корзину!')
    return redirect('catalog:product_list')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    
    messages.success(request, 'Товар удален из корзины!')
    return redirect('orders:cart')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Количество обновлено!')
        else:
            cart_item.delete()
            messages.success(request, 'Товар удален из корзины!')
    
    return redirect('orders:cart')

# Заглушки для будущих функций
def checkout(request):
    return render(request, 'orders/checkout.html')

def order_history(request):
    return render(request, 'orders/order_history.html')