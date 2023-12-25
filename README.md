# Присоединяйтесь к Upwork Project!

Приветствуем вас в нашем проекте Upwork! Мы создаем среду, где сотрудничество с фрилансерами становится простым и приятным процессом. Наш проект уже включает в себя:

- [![GitHub Actions](https://github.com/spadi23/Upwork/workflows/deployaws/badge.svg)](https://github.com/spadi23/Upwork/actions) Статус сборки проекта с использованием GitHub Actions
- [![Python Version](https://img.shields.io/badge/Python-3.10.12-blue)](https://www.python.org/) Используемая версия Python
- [![Django Version](https://img.shields.io/badge/Django-5-green)](https://www.djangoproject.com/) Используемая версия Django
- [![Last Commit](https://img.shields.io/github/last-commit/spadi23/Upwork)](https://github.com/spadi23/Upwork/commits/deployaws) Последний коммит в ветке deployaws
- и многое другое!

Присоединитесь к нам, чтобы сделать процесс работы с фрилансерами еще удобнее и эффективнее. Давайте вместе создадим успешные проекты и развиваемые команды!

[![Deploy Status](https://github.com/spadi23/Upwork/actions/workflows/deploy.yaml/badge.svg?branch=deployaws)](https://github.com/spadi23/Upwork/actions/workflows/deploy.yaml)
[![Статус Nginx](https://img.shields.io/badge/Nginx-Running-success)](https://nginx.org/)
[![Статус Celery](https://img.shields.io/badge/Celery-Running-success)](http://www.celeryproject.org/)
[![Redis Version](https://img.shields.io/badge/Redis-latest-red)](https://redis.io/)
[![Supervisor Version](https://img.shields.io/badge/Supervisor-latest-green)](http://supervisord.org/)


Наша платформа включает в себя инновационные инструменты для эффективного взаимодействия, управления задачами и обеспечения открытости коммуникации между заказчиками и исполнителями. Мы придаем особое внимание безопасности и удобству использования, чтобы каждый участник мог сосредоточиться на творческом процессе, не отвлекаясь на технические аспекты.

# Getting Started

    Project requirements

    Python 3.10.12
    Postgres SQL 15

    Steps to launch the project locally

    Clone repo
<!-- 
# git clone git@github.com:spadi23/Upwork.git
# git checkout deployaws -->


Установка Python зависимостей
    pip3 install -r requirements.txt


# Инструкция запуска проекта в режиме development

Заполнить настройки проекта:
    .env
Заполнить настройки соединения с БД Postgres:
    /config/setting.py

     DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',
            'PORT': '5432',
    }
}:

Перейти в папку /upwork и выполнить запуск миграций:

    python3 manage.py migrate

Выполнить установку Библиотек:

    pip3 install -r requirements

Перейти в корневую папку проекта и запустить:

    python3 manage.py runserver

# Примечания

При запуске  выполняется автоматическое создание пользователя с полными правами: создание, чтение, обновление и удаление на всех маршрутах приложения:
    email: admin@idea.com
    password: admin@idea.com

Для авторизации в приложении необходимо выполнить post-запрос по маршруту:

    http://localhost:8000/admin/login/?next=/admin/

body:

    {
    "email": "admin@idea.com",
    "password": "admin@idea.com"
    }

В теле ответа будет возвращен токен аутентификации для защищенных маршрутов приложения (описание маршрутов будет предоставлено отдельно)


Если вы делаете исправление, добавьте префикс **fix/**<br/>
Если вы реализуете новую функциональность, добавьте префикс **feature/**</br>
```
git checkout -b префикс/имя ветки
```

## Основные правила
1. Задавайте вопросы, как только они возникают, но перед этим потратьте ~30 минут на собственное расследование.
2. Сообщите о своей недоступности как можно скорее.
3. Будьте активны, продуктивны и получайте удовольствие.
4. Внесите все необходимые изменения и напишите разумный коммит. Старайтесь быть кратким, но записывайте в него ключевые изменения.
5. Отправьте изменения в репозиторий, создайте PR от **имя ветки** до **deployaws**.
6. Запросите на него проверку и сообщите о пиаре в чат, это ускорит наш процесс.
7. Прикрепите ссылку на задачу Trello к PR, а ссылку PR — к задаче Trello.
8. Если вы интегрируетесь с каким-либо сервисом/API, добавьте отдельную страницу в папку документации.
9. Объедините его в разработке.
10. Проверьте, всё ли в порядке в [Действиях]().


