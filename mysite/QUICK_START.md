# Быстрый старт - Django с Logging, Docker и Grafana Loki

## Шаг 1: Установка Loki Driver (Mac/Linux)

```bash
cd mysite/
bash scripts/install-loki-driver.sh
```

На **Windows** с Docker Desktop - driver уже установлен.

## Шаг 2: Запустить Docker Compose

```bash
# Находитесь в директории mysite/
cd mysite/

# Первый старт - соброит образы
docker-compose up --build

# Последующие старты
docker-compose up
```

### Осиновные сервисы:
- **Django**: http://localhost:8000
- **Debug Toolbar**: в правом верхнем углу приложения
- **Grafana** (Logs): http://localhost:3000
- **Loki API**: http://localhost:3100
- **PostgreSQL**: localhost:5432

## Шаг 3: Просмотр логов

### В консоли (Real-time):
```bash
docker-compose logs -f web
```

### В Grafana:
1. Откройте http://localhost:3000
2. В левом меню эксплорирования кликните **Explore**
3. От datasource выберите **Loki**
4. Напишите: `{service="django", app="mysite"}`
5. Нажмите **Run query**

### На машине (Логи в файле):
```bash
tail -f mysite/logs/django.log
```

## Проверка статуса контейнеров

```bash
docker-compose ps
```

Очидаемые контейнеры:
- `mysite_db` - PostgreSQL (healthy)
- `mysite_web` - Django (healthy)
- `mysite_grafana` - Grafana (healthy)
- `mysite_loki` - Loki (healthy)

## Настроенное

- ✅ **LOGGING**: Настроен в `settings.py` с подробным форматированием
- ✅ **Debug Toolbar**: Установлен и настроен
- ✅ **Docker**: Одномендные открытые
- ✅ **Grafana Loki**: Контейнеровые логи собираются от web сервиса

## Удаление всего

```bash
# Остановить контейнеры
docker-compose down

# Остановить + удалить volumes
docker-compose down -v

# Остановить + удалить images
docker-compose down -v --rmi all
```

## На что обратить внимание

1. **Django логи**: Откроются автоматически в консолях
2. **Debug Toolbar**: Нажмите панель в равом углу вы, чтобы открыть аналитику
3. **Grafana**: Мощные инструменты для крысталльных эталонности и поисковых логов

## Детальные инструкции

Осмотрите `SETUP_GUIDE.md` в этой директории для ополнительной информации.
