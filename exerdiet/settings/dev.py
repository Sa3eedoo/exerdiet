from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-$b@=t%v6434t@9(&y1c(!7dm!mni+vw)p*sxbil_6rw1-f2!l&'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'exerdiet',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '1234'
    }
}
