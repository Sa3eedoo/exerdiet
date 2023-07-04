from django.core.wsgi import get_wsgi_application
import os
import sys
import time
from dotenv import load_dotenv

project_folder = os.path.expanduser(
    '/home/exerdiet/exerdiet')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

# assuming your Django settings file is at '/home/myusername/mysite/mysite/settings.py'
path = '/home/exerdiet/exerdiet'
if path not in sys.path:
    sys.path.insert(0, path)

DJANGO_SETTINGS_MODULE = os.getenv("DJANGO_SETTINGS_MODULE")
TZ = os.getenv("TZ")
time.tzset()
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT")

application = get_wsgi_application()


# /static/	/home/exerdiet/exerdiet/static
# /media/	/home/exerdiet/exerdiet/static/media
# set -a; source /home/exerdiet/exerdiet/.env; set +a
# set -a; source /home/exerdiet/exerdiet/.env; set +a && /home/exerdiet/.virtualenvs/exerdiet/bin/python /home/exerdiet/exerdiet/manage.py update_streak
