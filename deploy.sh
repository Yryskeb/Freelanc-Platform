# зависимостi
# source venv/bin/activate
pip install -r requirements.txt
# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# pip uninstall Django
# pip install Django==5.0


# SECRET_KEY=${SECRET_KEY} \
# DEBUG=${DEBUG} \
# DB_NAME=${DB_NAME} \
# DB_USER=${DB_USER} \
# DB_PASSWORD=${DB_PASSWORD} \
# DB_HOST=${DB_HOST} \
# DB_PORT=${DB_PORT} \
# EMAIL_HOST_USER=${EMAIL_HOST_USER} \
# EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD} \
python3 manage.py migrate


# Gunicorn
sudo systemctl restart gunicorn

# Nginx
sudo systemctl restart nginx

# Supervisor
sudo systemctl restart supervisor

# Redis
sudo systemctl restart redis

# Celery
sudo supervisorctl restart celery