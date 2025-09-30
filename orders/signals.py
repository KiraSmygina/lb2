# orders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Cart
from django.db import IntegrityError, transaction

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        def _create():
            try:
                Cart.objects.get_or_create(user=instance)
            except IntegrityError:
                # Если БД ещё не готова, тихо пропускаем — корзина создастся при первом обращении
                pass
        transaction.on_commit(_create)