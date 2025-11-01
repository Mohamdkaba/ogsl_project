import os
os.system("python manage.py migrate --noinput")
os.system("python manage.py collectstatic --noinput")
