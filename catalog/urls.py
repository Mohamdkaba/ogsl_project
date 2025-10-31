from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SourceViewSet, OrganizationViewSet, ThemeViewSet, DatasetViewSet

router = DefaultRouter()
router.register(r'sources', SourceViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'themes', ThemeViewSet)
router.register(r'datasets', DatasetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
