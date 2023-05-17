import os
import sys

DJANGO_SETTINGS_MODULE = 'exerdiet.settings.dev'

# PWD = os.getenv("PWD")
PWD = "C:/Users/reema/Desktop/Graduation Project second term/Exerdiet"


def init():
    # os.chdir(PWD)
    sys.path.insert(0, PWD)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    import django
    django.setup()