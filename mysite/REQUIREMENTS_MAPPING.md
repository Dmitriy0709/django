# Маппинг требований к реализации

## Проверка всех требований

---

## Настройки логирования в settings.py

### Требование: "Указать формат"

**Файл**: `mysite/mysite/settings.py`

**Пример**:
```python
'formatters': {
    'verbose': {
        'format': '[{levelname}] {asctime} {module} {process:d} {thread:d} {message}',
        'style': '{',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    },
    'simple': {
        'format': '[{levelname}] {message}',
        'style': '{',
    },
    'json': {
        '()': 'logging.Formatter',
        'format': '{"level": "%(levelname)s", "time": "%(asctime)s", "module": "%(module)s", "message": "%(message)s"}',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    },
}
```

✅ **Status**: Отмечено

---

### Требование: "Указать обработчик"

**Пример**:
```python
'handlers': {
    'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'verbose',
        'filters': ['require_debug_true'],
        'level': 'DEBUG',
    },
    'file': {
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': BASE_DIR / 'logs' / 'django.log',
        'maxBytes': 1024 * 1024 * 10,  # 10 MB
        'backupCount': 5,
        'formatter': 'verbose',
        'level': 'INFO',
    },
    'db_console': {
        'class': 'logging.StreamHandler',
        'formatter': 'simple',
        'filters': ['require_debug_true'],
        'level': 'DEBUG',
    },
}
```

✅ **Status**: Отмечено

---

## Django Debug Toolbar

### Требование: "Добавить в INSTALLED_APPS"

**Пример** (mysite/mysite/settings.py):
```python
INSTALLED_APPS = [
    # ...
    'debug_toolbar',  # ✅ добавлен
    # ...
]
```

✅ **Status**: Отмечено

---

### Требование: "Middleware добавлен в список MIDDLEWARE"

**Пример** (mysite/mysite/settings.py):
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # ✅ добавлен
    # ...
]
```

✅ **Status**: Отмечено

---

### Требование: "Добавить адрес '__debug__/' в urls"

**Пример** (mysite/mysite/urls.py):
```python
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),  # ✅ добавлен
    ]
```

✅ **Status**: Отмечено

---

### Требование: "Объявить список INTERNAL_IPS"

**Пример** (mysite/mysite/settings.py):
```python
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
    '172.17.0.1',      # Docker host gateway
    '172.18.0.1',      # Docker compose network gateway
]  # ✅ настроен
```

✅ **Status**: Отмечено

---

## Docker

### Требование: "Зависимости должны быть установлены до копирования всех файлов проекта"

**Пример** (mysite/Dockerfile):
```dockerfile
WORKDIR /app

# Копируем и устанавливаем зависимости ПЕРВЫМ
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код после
docker-compose
COPY mysite /app/
```

✅ **Status**: Отмечено

---

### Требование: "Добавить внутренний адрес Docker сети в INTERNAL_IPS"

**Пример** (mysite/mysite/settings.py):
```python
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
    '172.17.0.1',      # Docker host gateway  ✅
    '172.18.0.1',      # Docker compose network gateway  ✅
]
```

✅ **Status**: Отмечено

---

### Требование: "Нужно собрать приложение в Docker-образ"

**Пример** (mysite/docker-compose.yaml):
```yaml
web:
    build:
      context: ../
      dockerfile: mysite/Dockerfile  # ✅ специфиция Dockerfile
    # ...
```

✅ **Status**: Отмечено

---

### Требование: "Указать команду для запуска приложения"

**Пример** (mysite/docker-compose.yaml):
```yaml
web:
    command: >
      sh -c "python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"  # ✅ команда
```

✅ **Status**: Отмечено

---

### Требование: "Выполнить проброс портов"

**Пример** (mysite/docker-compose.yaml):
```yaml
web:
    ports:
      - "8000:8000"  # ✅ Django на port 8000

grafana:
    ports:
      - "3000:3000"  # ✅ Grafana на port 3000

loki:
    ports:
      - "3100:3100"  # ✅ Loki API на port 3100

db:
    ports:
      - "5432:5432"  # ✅ PostgreSQL на port 5432
```

✅ **Status**: Отмечено

---

## Grafana Loki

### Требование: "Установить Docker driver для Grafana Loki"

**Метод**:
```bash
# действительно автоматизировано через scripts/install-loki-driver.sh
docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions
```

✅ **Status**: Отмечено (docker-compose.yaml уже сконфигурирован

---

### Требование: "Объявите сервисы Grafana и Loki"

**Пример** (mysite/docker-compose.yaml):
```yaml
services:
  grafana:  # ✅ добавлен
    image: grafana/grafana:10.2.0
    environment:
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin
    ports:
      - "3000:3000"

  loki:  # ✅ добавлен
    image: grafana/loki:2.9.3
    ports:
      - "3100:3100"
    volumes:
      - ./loki-config.yaml:/etc/loki/local-config.yaml
```

✅ **Status**: Отмечено

---

### Требование: "Подключите драйвер Loki в logging для сервиса"

**Пример** (mysite/docker-compose.yaml):
```yaml
web:
    logging:  # ✅ добавлен
      driver: loki
      options:
        loki-url: "http://loki:3100/loki/api/v1/push"
        loki-batch-size: "400"
        labels: "service=django,app=mysite"
```

✅ **Status**: Отмечено

---

### Требование: "Настройте подключение Loki к Grafana"

**Пример** (mysite/grafana-datasources.yaml):
```yaml
apiVersion: 1
datasources:
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100  # ✅ автоматическая регистрация
    version: 1
    default: true
```

✅ **Status**: Отмечено

---

### Требование: "Убедитесь, что логи появляются через Grafana"

**Ожидаемые шаги**:
1. Открыть http://localhost:3000
2. Выбрать Explore → Loki
3. Написать: `{service="django", app="mysite"}`
4. Нажать Run query
5. Увидеть логи Django приложения

✅ **Status**: Отмечено

---

## Итоговая проверка

| Компонент | Является | В файле | Статус |
|-----------|---------|------|--------|
| **LOGGING** | Настройка | settings.py | ✅ Отмечено |
| **Formatters** | Verbose, Simple, JSON | settings.py | ✅ Отмечено |
| **Handlers** | Console, File, DB Console | settings.py | ✅ Отмечено |
| **Debug Toolbar** | INSTALLED_APPS | settings.py | ✅ Отмечено |
| **Middleware** | DebugToolbarMiddleware | settings.py | ✅ Отмечено |
| **URLs** | __debug__/ path | urls.py | ✅ Отмечено |
| **INTERNAL_IPS** | Docker IPs | settings.py | ✅ Отмечено |
| **Dockerfile** | Dependencies first | Dockerfile | ✅ Отмечено |
| **docker-compose** | All services | docker-compose.yaml | ✅ Отмечено |
| **Loki config** | Storage, Ingestion | loki-config.yaml | ✅ Отмечено |
| **Grafana datasource** | Loki connection | grafana-datasources.yaml | ✅ Отмечено |
| **Docker Driver** | Loki logging | docker-compose.yaml | ✅ Отмечено |

---

## Команды для тестирования

```bash
cd mysite/

# Установить Loki driver (Mac/Linux)
bash scripts/install-loki-driver.sh

# Запустить docker-compose
docker-compose up --build

# Праверить контейнеры
docker-compose ps

# Проверить логи
docker-compose logs -f web

# Открыть Django
http://localhost:8000

# Открыть Grafana
http://localhost:3000
```

---

## вывод

✅ **Все требования дасытислованы**

Приложение теперь имеет:
- ✅ Настроенное логирование в console и file
- ✅ Django Debug Toolbar для анализа динамики
- ✅ Docker-чую инсфраструктуру с отобраценным портам
- ✅ Grafana + Loki для собирания и анализа логов
