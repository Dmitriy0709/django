from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Расширенная модель профиля пользователя
    Предоставляет дополнительные поля для персонализации пользователя
    Связь: один к одному с моделью User
    """
    # Связь с пользователем (один к одному)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )

    # Аватар пользователя
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Аватар пользователя'
    )

    # Биография
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Биография'
    )

    # Персональный сайт
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name='Персональный веб-сайт'
    )

    # Телефон
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Номер телефона'
    )

    # Дата рождения
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения'
    )

    # Местоположение
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Местоположение'
    )

    # Дата создания профиля
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )

    # Дата последнего обновления
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'


# Сигнал для автоматического создания профиля при создании пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Обработчик сигнала для создания профиля при регистрации нового пользователя
    """
    if created:
        Profile.objects.create(user=instance)


# Сигнал для сохранения профиля при сохранении пользователя
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Обработчик сигнала для сохранения профиля при обновлении пользователя
    """
    instance.profile.save()
