#!/bin/bash

# Установка зависимостей
pip3 install -r requirements.txt
sudo apt-get update
sudo apt-get install -y postgresql

# Проверка статуса PostgreSQL и, при необходимости, его запуск
if ! sudo service postgresql status; then
  sudo service postgresql start
fi

# Создание базы данных и пользователя
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'UTC';"

# Применение миграций Django
python3 manage.py migrate