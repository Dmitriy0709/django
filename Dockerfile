FROM python:3.11-slim

WORKDIR /app

# Установка Poetry одной строкой
RUN pip install --no-cache-dir --upgrade pip poetry && \
    poetry config virtualenvs.create false --local

# Копируем зависимости для кэша
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-interaction --no-ansi

# Копируем код
COPY . .

# Пользователь и права одной командой
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

WORKDIR /app/mysite

HEALTHCHECK CMD python manage.py shell -c "import django; django.setup(); print('OK')"
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
