# celery -A proj worker -l INFO   -   запуск наверное 

# 1. redis-server    -  на пустом терминале
# 2. make run 
# 3. python -m celery -A config worker -l info    -   venv activate

import os 
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.conf.broker_connection_retry_on_startup = True

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True, ingore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

