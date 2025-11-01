#!/usr/bin/env bash
set -o errexit

# Exécuter les migrations et collecter les fichiers statiques à chaque démarrage
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Démarrer l’application Django
gunicorn ogsl_core.wsgi:application
