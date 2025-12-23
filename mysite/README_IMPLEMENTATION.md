# Django Практическая работа: Logging, Debug Toolbar и Docker с Grafana Loki

## Что было реализовано

### 1. Логирование в Django

✅ **LOGGING configuration** в `settings.py` настроен с тремя видами форматирования:
- **verbose**: Полные инфо (time, module, PID, TID)
- **simple**: Минимальные сведения
- **json**: JSON формат для структурированных логов

**Обработчики**:
- **console**: Быстрые логи в DEBUG
- **file**: Ротационные логи (10 MB по макс)
- **db_console**: SQL достижимые логи

### 2. Django Debug Toolbar

✅ **Полною настроен**:
```python
# settings.py
INSTALLED_APPS = [..., 'debug_toolbar']
MIDDLEWARE = [..., 'debug_toolbar.middleware.DebugToolbarMiddleware']

# urls.py
if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

# settings.py
INTERNAL_IPS = ['127.0.0.1', 'localhost', '172.17.0.1', '172.18.0.1']
```

**Особенности**:
- Panel автоматически появляется в правом верхнем углу
- Анализ SQL, headers, settings
- Работает в Docker благодаря Docker gateway IPs

### 3. Docker и Docker Compose

✅ **Dockerfile**:
```dockerfile
- Установка зависимостей РЕРЕД копированием кода
- Health check
- Монтирование logs директории
```

✅ **docker-compose.yaml**:
```yaml
Services:
- db (PostgreSQL 16)
- web (Django)
- grafana (UI for logs)
- loki (Log storage)

Networking:
- Dedicated bridge network
- Health checks for dependencies

Logging:
- Loki driver for web service
- Persistent volumes for data
```

### 4. Grafana + Loki

✅ **Полные настройки**:

```yaml
# loki-config.yaml
- BoltDB Shipper backend
- Filesystem storage (/loki/chunks)
- 24-hour index periods
- Ingestion rate limits

# grafana-datasources.yaml
- Automatic Loki datasource registration
- Default datasource for Grafana
- LogQL query support
```

**Функциональность**:
- Логи анализируются через Grafana UI
- LogQL для гибких запросов
- Real-time monitoring

---

## Кортина архитектуры

```
┌───────────────────────┐
│   Docker Compose Network    │
│  (mysite-network bridge)   │
├───────────────────────┤
│                            │
│  ┌───────┐ ┌───────┐  │
│  │ Django  │ │ Postgres │  │
│  │  8000   │ │  5432   │  │
│  └───────┘ └───────┘  │
│         │            │        │
│      ┌─┘────┐ ┌─────┌───┐│
│      │   Loki    │ │ Grafana  │  │
│      │   3100   │ │   3000  │  │
│      └───────┘ └─────└───┘  │
│          │             │         │
└───────────────────────┘
      └─────┐
        │
Logging Driver (Loki)
Docker → Container stdout → Loki API
```

---

## Файлы

### Новые файлы

1. **loki-config.yaml** - Loki server configuration
2. **grafana-datasources.yaml** - Grafana datasource provisioning
3. **SETUP_GUIDE.md** - Complete setup instructions
4. **QUICK_START.md** - Fast start guide
5. **CHANGES_SUMMARY.md** - Summary of all changes
6. **REQUIREMENTS_MAPPING.md** - Requirement-to-implementation mapping
7. **scripts/install-loki-driver.sh** - Automated Loki driver installation

### Обновленные файлы

1. **mysite/settings.py** - LOGGING, INTERNAL_IPS
2. **mysite/Dockerfile** - Optimized, dependencies first
3. **docker-compose.yaml** - Services, Loki driver, networks

---

## Быстрый старт

### Шаг 1: Установить Loki Driver (Mac/Linux only)

```bash
cd mysite/
bash scripts/install-loki-driver.sh
```

### Шаг 2: Запустить Docker

```bash
docker-compose up --build
```

### Шаг 3: Открыть в браузере

- **Django**: http://localhost:8000
- **Grafana**: http://localhost:3000
- **API Docs**: http://localhost:8000/api/docs/

---

## Тестирование

### Проверить Логи

```bash
# В консоли
docker-compose logs -f web

# В файле
tail -f mysite/logs/django.log
```

### Проверить Grafana

1. Открыть http://localhost:3000
2. Explore → Loki
3. Написать: `{service="django", app="mysite"}`
4. Run query

### Проверить Debug Toolbar

1. Открыть http://localhost:8000
2. Панель в правом верхнем углу
3. От klik = Explore

---

## Особенности

### Гибкие LogQL запросы

```logql
# Все логи
{service="django", app="mysite"}

# Только ошибки
{service="django"} |= "ERROR"

# Запросы к БД
{app="mysite"} |= "db.backends"

# На последних 5 минут
{service="django"} | since 5m
```

### Ротационные логи

- Макс 10 MB за файл
- 5 backup files
- Автоматическая ротация

### Персистентные волюмы

- PostgreSQL data
- Grafana storage
- Loki chunks

---

## Цикл работы

```
1. Django приложение
   ↓
2. LOGGING configuration логирует в console + file
   ↓
3. Docker logging driver (Loki) передаёт логи
   ↓
4. Loki сохраняет них
   ↓
5. Grafana отображает кю LogQL
```

---

## Что дальше?

### Целные метрики

Можно добавить Prometheus для метрик:
```yaml
prometheus:
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"
```

### Алерты

Настроить alerts в Grafana для критических ошибок.

### Стэктрессинг

Одноредактированный Jaeger для распределённой трассировки.

---

## Документация

- `QUICK_START.md` - Быстрый старт
- `SETUP_GUIDE.md` - Подробная инструкция
- `CHANGES_SUMMARY.md` - Список изменений
- `REQUIREMENTS_MAPPING.md` - Соответствие требованиям

---

## Статус Выполнения

| Требование | Статус | Файл |
|------------|--------|------|
| LOGGING форматирование | ✅ | settings.py |
| LOGGING обработчики | ✅ | settings.py |
| Django Debug Toolbar | ✅ | settings.py, urls.py |
| Dockerfile оптимизация | ✅ | Dockerfile |
| docker-compose сервисы | ✅ | docker-compose.yaml |
| Grafana Loki | ✅ | docker-compose.yaml |
| Логирование контейнеров | ✅ | docker-compose.yaml |
| Просмотр в Grafana | ✅ | loki-config.yaml |

---

**Все требования выполнены! ✅**
