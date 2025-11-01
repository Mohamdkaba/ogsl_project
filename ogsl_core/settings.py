"""
Django settings pour le projet OGSL_API_ONLY
Version simplifiée — Déploiement API REST sur Render.com
"""

import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# =====================================================
# 🔧 Initialisation
# =====================================================
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================================
# 🔐 Sécurité & configuration
# =====================================================
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-temp-key")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".onrender.com"]

# =====================================================
# 🧩 Applications installées
# =====================================================
INSTALLED_APPS = [
    # Django de base
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # API REST
    "rest_framework",
    "drf_yasg",
    "django_filters",

    # Applications internes essentielles
    "harvest",
    "catalog",
]

# =====================================================
# ⚙️ Middleware
# =====================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =====================================================
# 🔗 URLs & WSGI
# =====================================================
ROOT_URLCONF = "ogsl_core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ogsl_core.wsgi.application"

# =====================================================
# 🗄️ Base de données
# =====================================================
# ✅ Par défaut : SQLite (local)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ✅ Si Render fournit DATABASE_URL (PostgreSQL), on l’utilise
if os.getenv("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config(
        conn_max_age=600, ssl_require=True
    )

# =====================================================
# 🔑 Authentification & mots de passe
# =====================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =====================================================
# 🌍 Internationalisation
# =====================================================
LANGUAGE_CODE = "fr"
TIME_ZONE = "America/Toronto"
USE_I18N = True
USE_TZ = True

# =====================================================
# 🧱 Fichiers statiques
# =====================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# =====================================================
# ⚙️ Django REST Framework
# =====================================================
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

# =====================================================
# ✅ Divers
# =====================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
