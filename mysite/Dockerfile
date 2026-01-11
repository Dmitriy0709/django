FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# ВАЖНО: Копируем requirements.txt ПЕРВЫМ для кеширования слоя
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
# ИСПРАВЛЕНО: Копируем весь проект, а не только mysite/
COPY . /app/

# Создаем необходимые директории
RUN mkdir -p /app/logs \
    && mkdir -p /app/staticfiles \
    && mkdir -p /app/uploads

# Создаем непривилегированного пользователя для безопасности
RUN useradd -m -u 1000 django && chown -R django:django /app
USER django

EXPOSE 8000

# Healthcheck для проверки работоспособности
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000').read()"

# Запуск через gunicorn
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
