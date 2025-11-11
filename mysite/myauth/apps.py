from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver


class MyauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myauth'
    verbose_name = 'Authentication'

    def ready(self):
        from django.contrib.auth.models import User
        from .models import Profile

        @receiver(post_save, sender=User)
        def create_user_profile(sender, instance, created, **kwargs):
            """
            Автоматически создаем профиль при создании пользователя.
            """
            if created:
                Profile.objects.get_or_create(user=instance)

        @receiver(post_save, sender=User)
        def save_user_profile(sender, instance, **kwargs):
            """
            Сохраняем профиль при сохранении пользователя.
            """
            try:
                instance.profile.save()
            except Profile.DoesNotExist:
                Profile.objects.create(user=instance)
