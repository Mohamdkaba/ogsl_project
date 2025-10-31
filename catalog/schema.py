import graphene
from graphene_django import DjangoObjectType
from catalog.models import Dataset, Source, Organization, Theme


# --- Définition des types GraphQL ---
class SourceType(DjangoObjectType):
    class Meta:
        model = Source
        fields = ("id", "name", "base_url", "is_active")


class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = ("id", "name", "website")


class ThemeType(DjangoObjectType):
    class Meta:
        model = Theme
        fields = ("id", "name")


class DatasetType(DjangoObjectType):
    class Meta:
        model = Dataset
        fields = (
            "id",
            "title",
            "description",
            "publication_date",
            "last_update",
            "url",
            "source",
            "organization",
            "themes",
        )


# --- Définition des requêtes disponibles ---
class Query(graphene.ObjectType):
    all_datasets = graphene.List(DatasetType)
    all_sources = graphene.List(SourceType)
    all_organizations = graphene.List(OrganizationType)
    all_themes = graphene.List(ThemeType)

    # Requête personnalisée : filtrer les datasets par source
    datasets_by_source = graphene.List(DatasetType, source_id=graphene.Int(required=True))

    def resolve_all_datasets(root, info):
        return Dataset.objects.all()

    def resolve_all_sources(root, info):
        return Source.objects.all()

    def resolve_all_organizations(root, info):
        return Organization.objects.all()

    def resolve_all_themes(root, info):
        return Theme.objects.all()

    def resolve_datasets_by_source(root, info, source_id):
        return Dataset.objects.filter(source_id=source_id)


# --- Création du schéma global ---
schema = graphene.Schema(query=Query)
