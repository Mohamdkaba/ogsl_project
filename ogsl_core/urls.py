from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

# --- API & GraphQL ---
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from graphene_django.views import GraphQLView

# --- Configuration Swagger ---
schema_view = get_schema_view(
    openapi.Info(
        title="OGSL API",
        default_version="v1",
        description="API pour la plateforme OGSL (catalogue de données ouvertes)",
        contact=openapi.Contact(email="contact@ogsl.ca"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# --- URL Patterns ---
urlpatterns = [
    # 🏠 Accueil (portail principal)

    path("", include(("portal.urls", "portal"))),
    path("portal/", include(("portal.urls", "portal"))),
 # page d’accueil du site OGSL

    # 🧭 Interface d’administration Django
    path("admin/", admin.site.urls),

    # 📦 API REST (Django REST Framework)
    path("api/", include("catalog.urls")),

    # 📊 Tableau de bord & visualisations
    path("dashboard/", include("dashboard.urls")),

    # ⚙️ Swagger / ReDoc (documentation automatique)
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

    # 🔗 GraphQL (interface et endpoint unifié)
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
