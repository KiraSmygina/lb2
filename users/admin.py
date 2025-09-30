# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.admin.models import LogEntry


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'name', 'surname', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('name', 'surname', 'patronymic')
        }),
    )

    def delete_model(self, request, obj):
        # Удаляем связанные логи админки и предметные сущности до удаления пользователя
        LogEntry.objects.filter(user_id=obj.pk).delete()
        try:
            from orders.models import Cart, Order
            Cart.objects.filter(user=obj).delete()
            Order.objects.filter(user=obj).delete()
        except Exception:
            pass
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        # Массовое удаление: сначала чистим зависимости
        ids = list(queryset.values_list('pk', flat=True))
        LogEntry.objects.filter(user_id__in=ids).delete()
        try:
            from orders.models import Cart, Order
            Cart.objects.filter(user_id__in=ids).delete()
            Order.objects.filter(user_id__in=ids).delete()
        except Exception:
            pass
        super().delete_queryset(request, queryset)