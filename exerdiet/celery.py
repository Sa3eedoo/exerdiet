# import os 
# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exerdiet.settings')

# celery = Celery('exerdiet')
# celery.config_from_object('django.conf:settings', namespace='CELERY')
# celery.autodiscover_tasks()

import os
from decouple import config # python-dotenv
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exerdiet.settings.dev')

app = Celery('exerdiet')

# CELERY_
app.config_from_object("django.conf:settings", namespace='CELERY')

# app.conf.broker_url = ''
# app.conf.result_backend ='django-db'
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "run_movie_rating_avg_every_30": {
        'task': 'task_calculate_movie_ratings',
        'schedule': 30, # 30 min,
        'kwargs': {"all": True}
    }
}