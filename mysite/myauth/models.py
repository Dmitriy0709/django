from django.db import models
from django.contrib.auth.models import User


def user_avatar_upload_path(instance, filename):
    """
    Кастомная функция для генерации пути загрузки аватарки.
    Сохраняет в формате: avatars/user_{id}/{filename}
    """
    return f'avatars/user_{instance.user.id}/{filename}'


class Profile(models.Model):
    """
    Модель профиля для расширения стандартной модели User.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, verbose_name='О себе')
    avatar = models.ImageField(
        upload_to=user_avatar_upload_path,
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
