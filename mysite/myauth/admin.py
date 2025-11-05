"""
Админ-панель приложения myauth (аутентификация)
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    """
    Встроенный редактор для модели Profile
    Позволяет редактировать профиль прямо со страницы пользователя
    """
    model = Profile
    # Поля, которые будут отображаться в админ-панели
    fields = ('avatar', 'bio', 'website', 'phone', 'birth_date', 'location')
    # Количество пустых форм для добавления новых профилей
    extra = 0


class UserAdmin(BaseUserAdmin):
    """
    Расширенный админ-интерфейс для пользователей с встроенным редактором профиля
    """
    # Добавление встроенного редактора Profile
    inlines = [ProfileInline]


# Переустановка админ-интерфейса пользователя с профилем
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для модели Profile
    """
    # Поля, отображаемые в списке профилей
    list_display = ('user', 'location', 'phone', 'created_at', 'updated_at')

    # Фильтры на странице списка
    list_filter = ('created_at', 'updated_at')

    # Поля для поиска
    search_fields = ('user__username', 'user__email', 'location')

    # Поля, которые нельзя редактировать
    readonly_fields = ('user', 'created_at', 'updated_at')

    # Организация полей в группы
    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Личная информация', {
            'fields': ('avatar', 'bio', 'website', 'phone', 'birth_date', 'location')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Свернуть по умолчанию
        }),
    )
