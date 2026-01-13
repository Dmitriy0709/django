# 🐳 Решение проблемы "Container name already in use"

## 🔴 Ваша Ошибка

```
ERROR: Cannot create container for service db: Conflict. 
The container name "/mysite_db" is already in use by container "867580ef458e50720549573fbcb04b1110d7f727088506caa3eabf3f623174eb"
```

**Причина:** Старые контейнеры остались на диске и конфликтуют с новыми.

---

## ✅ РЕШЕНИЕ (Выполните Строго по Порядку)

### Шаг 1️⃣: Удалить все старые контейнеры

```bash
cd ~/PycharmProjects/django

# Удалить старые контейнеры вручную
docker rm mysite_web
docker rm mysite_db
docker rm mysite_grafana

# Или все сразу (если они остановлены)
docker rm mysite_web mysite_db mysite_grafana

# Вывод должен быть:
# mysite_web
# mysite_db
# mysite_grafana
```

### Шаг 2️⃣: Удалить старые тома

```bash
# Удалить старые тома
docker volume rm mysite_postgres_data
docker volume rm mysite_grafana_storage
docker volume rm mysite_loki_storage

# Вывод:
# mysite_postgres_data
# mysite_grafana_storage
# mysite_loki_storage
```

### Шаг 3️⃣: Проверить что удалилось

```bash
# Должно быть пусто
docker ps -a

# Должны остаться только новые тома (django_*)
docker volume ls
```

### Шаг 4️⃣: Теперь запустить заново

```bash
# Запустить контейнеры
docker-compose up -d

# Проверить статус
docker-compose ps

# Должно показать ВСЕ три сервиса с STATUS "Up"
```

---

## 🎯 Полная Команда за Раз

Если хотите выполнить всё одной командой:

```bash
cd ~/PycharmProjects/django && \
docker rm -f mysite_web mysite_db mysite_grafana 2>/dev/null; \
docker volume rm mysite_postgres_data mysite_grafana_storage mysite_loki_storage 2>/dev/null; \
sleep 1 && \
docker-compose up -d && \
sleep 3 && \
docker-compose ps
```

---

## 📊 Что Произойдёт После Удаления

✅ `docker rm -f` - удалит старые контейнеры (флаг `-f` = force)
✅ `docker volume rm` - удалит старые тома с данными
✅ `docker-compose up -d` - создаст новые контейнеры с новыми названиями
✅ `docker-compose ps` - покажет статус

---

## 🔍 Если Всё Ещё Не Работает

```bash
# Полная ядерная очистка Docker
docker system prune -a --volumes -f

# Потом:
cd ~/PycharmProjects/django
docker-compose up -d
```

---

## ✅ Признаки Успеха

После `docker-compose ps` должны увидеть:

```
NAME                COMMAND                  SERVICE   STATUS
mysite_db           "docker-entrypoint.s…"   db        Up (healthy)
mysite_web          "sh -c 'python..."       web       Up
mysite_grafana      "/run.sh"                grafana   Up
```

**ВСЕ должны быть "Up" - это УСПЕХ!** ✅

---

## 🚀 Проверить Приложение

После успешного старта:

```bash
# Проверить логи
docker-compose logs web | tail -20

# Если видите "Listening on", значит работает!

# Попробовать открыть в браузере
# http://localhost:8000/
```

---

## 📞 Если Контейнеры Запустились но Приложение Не Работает

```bash
# Посмотреть логи веб-сервиса
docker-compose logs web

# Посмотреть логи БД
docker-compose logs db

# Зайти в контейнер и исправить вручную
docker-compose exec web bash

# Внутри контейнера:
cd mysite
python manage.py migrate
python manage.py createsuperuser
exit
```

---

**Напишите результат после выполнения команд!** 🎯