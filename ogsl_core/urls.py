from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.http import HttpResponseRedirect

# --- Configuration Swagger ---
schema_view = get_schema_view(
    openapi.Info(
        title="OGSL API",
        default_version="v1",
        description="Documentation de l’API REST de la plateforme OGSL",
        contact=openapi.Contact(email="contact@ogsl.ca"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # 🧭 Interface d’administration Django
    path("admin/", admin.site.urls),

    # 📦 API REST principale (tes endpoints DRF)
    path("api/", include("catalog.urls")),

    # 📚 Documentation Swagger & Redoc
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),

    # 🏠 Redirection accueil → Swagger
    path("", lambda request: HttpResponseRedirect("/swagger/")),
]
