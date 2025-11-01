"""
Django settings for ogsl_core project – version adaptée pour Render.com
"""

import os
from pathlib import Path
import dj_database_url  # 🔹 Nécessaire pour utiliser la DB Render
from dotenv import load_dotenv

# Charger les variables d’environnement (.env)
load_dotenv()

# --- Répertoire racine du projet ---
BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================================
# 🔐 Sécurité & configuration générale
# =====================================================
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-7p@y41=9mkh*51=zk%%&n%pre2^%*-2!*3g=#7$0dcbyf))jsw")

# En prod, DEBUG doit être False
DEBUG = os.getenv("DEBUG", "False") == "True"

# Autoriser Render + localhost
ALLOWED_HOSTS = ["ogsl-project.onrender.com", "localhost", "127.0.0.1"]



# =====================================================
# 🧩 Applications installées
# =====================================================
INSTALLED_APPS = [
    # --- Thème visuel Admin ---
    "colorfield",
    "admin_interface",

    # --- Apps Django par défaut ---
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # --- Frameworks externes ---
    "rest_framework",
    "drf_yasg",
    "graphene_django",

    # --- Applications internes ---
    "harvest",
    "catalog",
    "dashboard",
    "portal",
]


# =====================================================
# ⚙️ Middleware
# =====================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # 🔹 pour servir les fichiers statiques sur Render
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =====================================================
# 🔗 URLS / WSGI
# =====================================================
ROOT_URLCONF = "ogsl_core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
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
# Par défaut : MySQL local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # ✅ On garde ça
        'NAME': 'ogsl_db',
        'USER': 'root',
        'PASSWORD': 'admin123',
        'HOST': 'localhost',
        'PORT': '3306',


    }
}

# 🔹 Si Render fournit une base PostgreSQL (variable DATABASE_URL), on l’utilise automatiquement
if os.getenv("DATABASE_URL"):
    import dj_database_url
    DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# 🔹 Si on est sur Render (DATABASE_URL = PostgreSQL)
database_url = os.getenv("DATABASE_URL")
if database_url:
    DATABASES["default"] = dj_database_url.config(
        default=database_url,
        conn_max_age=600,
        ssl_require=False if 'mysql' in database_url else True
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
# 🧱 Fichiers statiques (CSS, JS, images)
# =====================================================
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "portal/static"]

# WhiteNoise : compression + cache
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# =====================================================
# 🧩 Django REST Framework
# =====================================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}


# =====================================================
# 🔮 GraphQL
# =====================================================
GRAPHENE = {
    "SCHEMA": "catalog.schema.schema",
}


# =====================================================
# ✅ Divers
# =====================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEBUG = os.getenv("DEBUG", "False") == "True"
