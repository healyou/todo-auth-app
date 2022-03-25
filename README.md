# Запуск приложения

## Запуск unit-тестов (mock объекты на взаимодействии приложения с внешними системами)
1) Активировать виртуальное окружение:
    'venv/Scripts/activate'
2) Установить необходимые зависимости в venv:
    'pip install -r requirements.txt'
3) Запустить unit тесты:
    'python -m pytest -c ./test/pytest_unit_test.ini'

## Запуск интеграционных тестов (redis + app, без других зависимых сервисов)
1) Активировать виртуальное окружение:
    'venv/Scripts/activate'
2) Установить необходимые зависимости в venv:
    'pip install -r requirements.txt'
3) Запустить redis через докер (из папки /db/redis/):
    'docker compose up -d'
4) Запустить интеграционные тесты:
    'python -m pytest -c ./test/pytest_integration_test.ini'

## Запуск интеграционных тестов со всеми зависимыми приложениями
1) Активировать виртуальное окружение:
    'venv/Scripts/activate'
2) Установить необходимые зависимости в venv:
    'pip install -r requirements.txt'
3) Запустить необходимые зависимости для сервиса (бд + users-app)
    запустить бд на docker (из папки /db/redis/) 'docker compose up -d'
    запустить users-app на docker
4) Запустить интеграционные тесты:
    'python -m pytest'
    Запустит DEV профиль, при этом ни одна зависимость не будет мокироваться в тестах

## Запуск приложения для разработки
1) Активировать виртуальное окружение:
    'venv/Scripts/activate'
2) Установить необходимые зависимости в venv:
    'pip install -r requirements.txt'
3) Запустить необходимые зависимости для сервиса (бд + users-app)
    запустить бд на docker (из папки /db/redis/) 'docker compose up -d'
    запустить users-app на docker
4) Запуск приложения:
    'python run.py'
5) Приложение будет принимать запросы по url:
    http://localhost:8887/auth

## Запуск в докере
1) Собрать docker image (из корня проекта):
    'docker build -t auth-app:v1 .'
2) Запустить redis + app на docker (из корня проекта):
    'docker compose up -d'
3) Запустить необходимые зависимости для сервиса (бд + users-app)
    запустить users-app на docker
4) Приложение будет принимать запросы по url:
    http://localhost:8887/auth
