# Файл: ./Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Копируем requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Команда для запуска
CMD ["sh", "-c", "\
    python mysite/manage.py migrate && \
    python mysite/manage.py collectstatic --noinput && \
    gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120"]
