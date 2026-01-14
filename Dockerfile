FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN cd mysite && python manage.py migrate && python manage.py collectstatic --noinput

CMD ["sh", "-c", "cd /app/mysite && gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120"]
