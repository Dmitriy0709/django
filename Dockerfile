FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip poetry && \ poetry config virtualenvs.create false --local

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-interaction --no-ansi

COPY . .


RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

WORKDIR /app/mysite

HEALTHCHECK CMD python manage.py shell -c "import django; django.setup(); print('OK')"
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0.8000", "--workers",
"4", "--timeout", "120"]
