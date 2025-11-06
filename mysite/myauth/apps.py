from django.apps import AppConfig


class MyauthConfig(AppConfig):
    """
    Конфигурация приложения myauth
    Содержит настройки приложения аутентификации и профилей пользователей
    """
    # Тип поля ID по умолчанию для новых моделей
    default_auto_field = 'django.db.models.BigAutoField'

    # Имя приложения
    name = 'myauth'

    # Человекочитаемое имя приложения в админ-панели
    verbose_name = 'Аутентификация и профили'
