import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# ========== APPLICATION DEFINITION ==========

INSTALLED_APPS = [
    # Django стандартные приложения
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ========== ПОЛЬЗОВАТЕЛЬСКИЕ ПРИЛОЖЕНИЯ ==========
    # Приложение аутентификации и профилей пользователей
    'myauth.apps.MyauthConfig',  # или просто 'myauth'

    # Приложение магазина товаров
    'shopapp',

    # Приложение req (если есть)
    'req',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'  # Замените 'mysite' на имя вашего проекта

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Глобальные шаблоны
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # ========== ВАЖНО: для доступа к MEDIA_URL в шаблонах
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'  # Замените 'mysite' на имя вашего проекта


# ========== DATABASE ==========
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Для PostgreSQL используйте:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'mysite_db',
#         'USER': 'postgres',
#         'PASSWORD': 'your_password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# ========== PASSWORD VALIDATION ==========
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ========== INTERNATIONALIZATION ==========
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'  # Русский язык

TIME_ZONE = 'Asia/Almaty'  # Измените на ваш часовой пояс

USE_I18N = True

USE_TZ = True


# ========== STATIC FILES (CSS, JavaScript, Images) ==========
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# URL для доступа к статическим файлам (CSS, JS)
STATIC_URL = '/static/'

# Папка для статических файлов приложений
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Папка, куда collectstatic соберёт все статические файлы для production
STATIC_ROOT = BASE_DIR / 'staticfiles'


# ========== MEDIA FILES (User Uploaded Content) ==========
# Для загрузки пользовательских файлов (аватары, изображения товаров)

# URL для доступа к медиа файлам
# Например: http://localhost:8000/media/avatars/user1.jpg
MEDIA_URL = '/media/'

# Папка для хранения загруженных файлов
MEDIA_ROOT = BASE_DIR / 'media'


# ========== AUTHENTICATION SETTINGS ==========

# URL для редиректа неавторизованных пользователей
# Когда используется @login_required декоратор
LOGIN_URL = 'myauth:login'

# URL для редиректа после успешного входа
LOGIN_REDIRECT_URL = '/'  # Главная страница

# URL для редиректа после выхода из системы
LOGOUT_REDIRECT_URL = 'myauth:login'


# ========== SESSION SETTINGS ==========

# Время жизни сессии (в секундах)
SESSION_COOKIE_AGE = 1209600  # 2 недели

# Сессия истекает при закрытии браузера
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Имя cookie для сессии
SESSION_COOKIE_NAME = 'sessionid'


# ========== EMAIL SETTINGS ==========
# Для отправки писем (password reset)

# Для разработки: вывод писем в консоль
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Для production (Gmail):
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'
# DEFAULT_FROM_EMAIL = 'your-email@gmail.com'


# ========== MESSAGES FRAMEWORK ==========
# Для вывода сообщений пользователю

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',  # Bootstrap класс для ошибок
}


# ========== DEFAULT PRIMARY KEY FIELD TYPE ==========
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ========== LOGGING CONFIGURATION ==========
# Для отладки и логирования ошибок

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# ========== SECURITY SETTINGS ==========
# Раскомментируйте для production

# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True


# ========== FILE UPLOAD SETTINGS ==========

# Максимальный размер загружаемого файла (в байтах)
# 5 MB = 5 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880

# Разрешённые расширения для загрузки изображений
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']


# ========== CUSTOM SETTINGS ==========
# Добавьте свои настройки здесь

# Количество элементов на странице при пагинации
PAGINATE_BY = 12

# Имя сайта
SITE_NAME = 'MyShop'


# ========== DEVELOPMENT/PRODUCTION ENVIRONMENT ==========

# Используйте переменные окружения для production
# import os
# SECRET_KEY = os.environ.get('SECRET_KEY')
# DEBUG = os.environ.get('DEBUG', 'False') == 'True'
# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
