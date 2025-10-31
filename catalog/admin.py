from django.contrib import admin
from .models import Source, Organization, Theme, Dataset

# === SOURCE ===
@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("name", "base_url", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("name",)


# === ORGANIZATION ===
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "website")
    search_fields = ("name",)
    ordering = ("name",)


# === THEME ===
@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


# === DATASET ===
@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("title", "source", "organization", "publication_date", "last_update")
    search_fields = ("title", "description")
    list_filter = ("source", "themes", "organization")
    ordering = ("-publication_date",)
    date_hierarchy = "publication_date"
