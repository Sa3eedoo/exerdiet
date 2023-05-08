import os
from .common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['exerdiet.pythonanywhere.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'exerdiet$exerdiet',
        'USER': 'exerdiet',
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': 'exerdiet.mysql.pythonanywhere-services.com',
    }
}
