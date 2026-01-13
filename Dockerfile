# Multi-stage build для оптимизации размера образа
FROM python:3.12-slim as builder

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Установка системных зависимостей для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt для кеширования слоя
COPY requirements.txt .

# Устанавливаем зависимости в виртуальное окружение
RUN pip install --user --no-cache-dir -r requirements.txt

# ════════════════════════════════════════════════════════════════
# Final stage - runtime образ
# ════════════════════════════════════════════════════════════════
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# Установка только runtime зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем установленные пакеты из builder стадии
COPY --from=builder /root/.local /root/.local

# Обновляем PATH
ENV PATH=/root/.local/bin:$PATH

# Копируем весь код приложения
COPY . /app/

# Создаем необходимые директории
RUN mkdir -p /app/logs \
    && mkdir -p /app/staticfiles \
    && mkdir -p /app/uploads \
    && mkdir -p /app/mysite/database

# Создаем непривилегированного пользователя для безопасности
RUN useradd -m -u 1000 django && chown -R django:django /app
USER django

EXPOSE 8000

# Healthcheck - проверка доступности приложения
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Запуск приложения через gunicorn
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
