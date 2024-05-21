Как запустить проект:
1. git clone https://github.com/vladislav-ml/vlondin17-test-o-parser
2. Установка docker и docker compose
3. Выполняем следующие команды в терминале:
- docker compose build
- docker compose create
- docker compose start
- ждем пару минут
- Выполняем команду docker compose ps -a
- Находим контейнер "web", отвечает за django и переходим в него:
Команда:
docker exec -it "название контейнера web" /bin/bash
Выполняем миграции и создаем пользователя:
 - python manage.py migrate
 - python manage.py createsuperuser

Перезапускаем.
docker compose restart

Телеграм бот находится по адресу:
t.me/django_test1_bot

