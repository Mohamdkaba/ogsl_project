import os

print("=== Applying database migrations on Render ===")
os.system("python manage.py makemigrations --noinput")
os.system("python manage.py migrate --noinput")
os.system("python manage.py collectstatic --noinput")
print("=== Migrations and static collection completed ===")
