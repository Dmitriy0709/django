# Django Application Setup Guide: Logging, Debug Toolbar & Docker with Grafana Loki

## Содержание
1. [Конфигурация логирования](#конфигурация-логирования)
2. [Django Debug Toolbar](#django-debug-toolbar)
3. [Docker и Docker Compose](#docker-и-docker-compose)
4. [Grafana Loki логирование](#grafana-loki-логирование)
5. [Запуск приложения](#запуск-приложения)
6. [Просмотр логов](#просмотр-логов)

---

## Конфигурация логирования

### Что было сделано в `settings.py`

#### 1. **Форматировщики (Formatters)**

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

- **verbose**: Полный формат с временем, процессом и потоком
- **simple**: Минимальный формат (уровень + сообщение)
- **json**: JSON формат для структурированных логов

#### 2. **Фильтры (Filters)**

```python
'filters': {
    'require_debug_true': {
        '()': 'django.utils.log.CallbackFilter',
        'callback': lambda record: DEBUG,
    },
    'require_debug_false': {
        '()': 'django.utils.log.CallbackFilter',
        'callback': lambda record: not DEBUG,
    },
}
```

- `require_debug_true`: Логирует только если DEBUG=True (для разработки)
- `require_debug_false`: Логирует только если DEBUG=False (для production)

#### 3. **Обработчики (Handlers)**

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

- **console**: Логирование в консоль в DEBUG режиме
- **file**: Логирование в файлы с ротацией (по 10 MB)
- **db_console**: Отдельный обработчик для БД логов

#### 4. **Логгеры (Loggers)**

```python
'loggers': {
    'django': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
        'propagate': False,
    },
    'django.db.backends': {
        'handlers': ['db_console'],
        'level': 'DEBUG',
        'propagate': False,
    },
    'django.request': {
        'handlers': ['console', 'file'],
        'level': 'WARNING',
        'propagate': False,
    },
    'mysite': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
        'propagate': False,
    },
}
```

#### 5. **Создание директории логов**

```python
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)
```

---

## Django Debug Toolbar

### Что уже настроено

✅ **INSTALLED_APPS**: `'debug_toolbar'` добавлен

✅ **MIDDLEWARE**: `'debug_toolbar.middleware.DebugToolbarMiddleware'` добавлен в список

✅ **URLs**: В `mysite/urls.py` добавлена строка:
```python
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
```

✅ **INTERNAL_IPS**: Настроен для локальной разработки И Docker:
```python
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
    '172.17.0.1',      # Docker host gateway
    '172.18.0.1',      # Docker compose network gateway
]
```

### Как использовать Debug Toolbar

1. Откройте приложение в браузере: `http://localhost:8000`
2. В правом верхнем углу страницы появится панель инструментов
3. Можно просмотреть:
   - SQL запросы и их время выполнения
   - HTTP headers
   - Settings
   - Cache
   - Signals
   - Logging

---

## Docker и Docker Compose

### Dockerfile оптимизация

**Ключевые практики:**

1. **Установка зависимостей ПЕРЕД копированием кода**
   ```dockerfile
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   ```
   - Docker кэширует слои, это позволяет быстро пересобирать образ если requirements не изменился

2. **Создание директории логов**
   ```dockerfile
   RUN mkdir -p /app/logs
   ```

3. **Health check**
   ```dockerfile
   HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
       CMD python -c "import requests; requests.get('http://localhost:8000')"
   ```

### Docker Compose сервисы

#### 1. **PostgreSQL (db)**
- Хранит данные приложения
- Health check для проверки готовности
- Порт: 5432

#### 2. **Django Web Application (web)**
- Запускает миграции и сервер приложения
- Подключен к Loki для логирования
- Volume маунтинг для development
- INTERNAL_IPS настроены в settings

#### 3. **Grafana**
- Web интерфейс для просмотра логов
- Доступна на: `http://localhost:3000`
- Анонимный доступ включен

#### 4. **Loki**
- Получает логи через Docker logging driver
- Хранит логи в `/loki`
- API на порту 3100

---

## Grafana Loki логирование

### Как работает

1. **Docker logging driver (Loki)** отправляет логи из контейнера
   ```yaml
   logging:
     driver: loki
     options:
       loki-url: "http://loki:3100/loki/api/v1/push"
       labels: "service=django,app=mysite"
   ```

2. **Loki** принимает логи и хранит их
   - Конфигурация: `loki-config.yaml`
   - Хранилище: `/loki/chunks` и `/loki/boltdb-shipper-active`

3. **Grafana** подключается к Loki как datasource
   - Конфигурация: `grafana-datasources.yaml`
   - Автоматически добавляет Loki при запуске

### Требования Docker driver Loki

#### На Mac/Linux:

```bash
# Установка Docker Compose Plugin (если использует docker compose)
docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions
```

#### На Windows с Docker Desktop:
- Docker Desktop уже включает поддержку Loki драйвера

---

## Запуск приложения

### Шаг 1: Подготовка

```bash
cd mysite/
```

### Шаг 2: Запуск Docker Compose

```bash
# Первый запуск (будет собран образ)
docker-compose up --build

# Последующие запуски
docker-compose up
```

### Шаг 3: Проверка статуса

```bash
# Проверить контейнеры
docker-compose ps

# Просмотреть логи
docker-compose logs -f web
```

---

## Просмотр логов

### 1. Логи Django в консоли (DEBUG режим)

Будут автоматически выводиться в консоль благодаря обработчику `console` в LOGGING конфигурации.

### 2. Файловые логи

Логи сохраняются в `mysite/logs/django.log`:

```bash
tail -f mysite/logs/django.log
```

### 3. Логи в Docker контейнере

```bash
# Просмотр всех логов контейнера
docker logs mysite_web

# Live follow
docker logs -f mysite_web
```

### 4. Логи в Grafana (через Loki)

1. Откройте Grafana: `http://localhost:3000`
2. В левом меню выберите **Explore**
3. В datasource выберите **Loki**
4. Напишите query для поиска логов:
   ```logql
   {service="django", app="mysite"}
   ```
5. Нажмите **Run query**

### Примеры LogQL queries:

```logql
# Все логи приложения
{service="django", app="mysite"}

# Только ошибки
{service="django", app="mysite"} |= "ERROR"

# Логи за последние 5 минут
{service="django", app="mysite"} | since 5m

# Запросы к БД
{service="django", app="mysite"} |= "db.backends"

# Warnings и Errors
{service="django", app="mysite"} |= "WARNING" or "ERROR"
```

---

## Проверочный список (Checklist)

### settings.py
- ✅ LOGGING настроен с форматами
- ✅ Обработчики для console и file
- ✅ Фильтры для DEBUG режима
- ✅ INTERNAL_IPS включает Docker сети
- ✅ Директория логов создана

### Django Debug Toolbar
- ✅ В INSTALLED_APPS
- ✅ Middleware добавлен
- ✅ URLs включены
- ✅ INTERNAL_IPS настроены

### Docker
- ✅ Dockerfile: зависимости устанавливаются первыми
- ✅ docker-compose.yaml включает все сервисы
- ✅ Loki driver настроен
- ✅ Grafana datasource настроен
- ✅ Networks настроены

### Grafana Loki
- ✅ Loki сервис запущен
- ✅ Docker driver для логирования
- ✅ Grafana подключена к Loki
- ✅ Logs директория смонтирована

---

## Troubleshooting

### Логи не появляются в Grafana

1. Проверьте, что Loki запущен:
   ```bash
   docker-compose ps | grep loki
   ```

2. Проверьте логи Loki:
   ```bash
   docker-compose logs loki
   ```

3. Убедитесь, что Docker driver установлен (Mac/Linux)

### Debug Toolbar не появляется

1. Проверьте DEBUG=True в настройках
2. Проверьте INTERNAL_IPS в settings.py
3. Очистите кэш браузера
4. Убедитесь, что middleware в правильном порядке

### Контейнер не запускается

1. Проверьте логи:
   ```bash
   docker-compose logs web
   ```

2. Убедитесь, что ports свободны (8000, 3000, 3100, 5432)

3. Очистите volumes:
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

---

## Дополнительные ресурсы

- [Django Logging Documentation](https://docs.djangoproject.com/en/stable/topics/logging/)
- [Django Debug Toolbar Documentation](https://django-debug-toolbar.readthedocs.io/)
- [Grafana Loki Documentation](https://grafana.com/docs/loki/latest/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
