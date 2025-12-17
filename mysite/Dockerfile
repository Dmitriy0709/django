FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt из КОРНЯ (так как context = ../)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое mysite/ в /app/
COPY mysite /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
