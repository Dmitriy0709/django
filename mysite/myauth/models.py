from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Расширенная модель профиля пользователя
    Предоставляет дополнительные поля для персонализации
    Связь один-к-одному с моделью User
    """
    # Связь с пользователем (один к одному)
    # При удалении пользователя удалится и профиль (CASCADE)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )

    # Биография пользователя
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Биография'
    )

    # Аватар (фотография профиля)
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Аватар'
    )

    # Дата рождения пользователя
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения'
    )

    # Персональный веб-сайт
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name='Веб-сайт'
    )

    # Телефон пользователя
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон'
    )

    # Местоположение пользователя
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

    # Дата последнего обновления профиля
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'


# ========== СИГНАЛЫ ДЛЯ АВТОМАТИЧЕСКОГО СОЗДАНИЯ ПРОФИЛЯ ==========

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Сигнал для автоматического создания профиля при создании пользователя
    Вызывается при регистрации нового пользователя
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Сигнал для сохранения профиля при сохранении пользователя
    Гарантирует синхронизацию профиля с пользователем
    """
    instance.profile.save()
