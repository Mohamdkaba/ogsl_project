from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="dashboard_index"),
    path("data/datasets_by_source/", views.datasets_by_source, name="datasets_by_source"),
    path("datasets-by-theme/", views.datasets_by_theme, name="datasets_by_theme"),
    path("data/datasets_by_theme_filtered/<int:source_id>/", views.datasets_by_theme_filtered, name="datasets_by_theme_filtered"),
    path('map/', views.map_view, name='dashboard_map'),
]
