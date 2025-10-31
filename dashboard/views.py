from django.shortcuts import render
from django.http import JsonResponse
from catalog.models import Dataset, Source, Organization, Theme
import json
from django.core.serializers.json import DjangoJSONEncoder




def index(request):
    """Vue principale du tableau de bord"""
    sources_count = Source.objects.count()
    organizations_count = Organization.objects.count()
    themes_count = Theme.objects.count()
    datasets_count = Dataset.objects.count()
    sources = Source.objects.all()

    context = {
        "sources_count": sources_count,
        "organizations_count": organizations_count,
        "themes_count": themes_count,
        "datasets_count": datasets_count,
        "sources": sources,
    }
    return render(request, "dashboard/index.html", context)


def datasets_by_source(request):
    """📊 Données pour le graphique : nombre de jeux de données par source (normalisées)"""
    rename_map = {
        "Open Gouv": "OpenGouv",
        "open gouv": "OpenGouv",
        "OpenGouv": "OpenGouv",
        "CanWin": "CanWin",
        "Données Québec": "Données Québec",
        "Donnees Quebec": "Données Québec",
        "Boréalis": "Boréalis",
        "Borealis": "Boréalis",
    }

    sources = Source.objects.all()

    labels = []
    counts = []

    for s in sources:
        name = rename_map.get(s.name, s.name)  # normalisation du nom
        count = Dataset.objects.filter(source=s).count()
        labels.append(name)
        counts.append(count)

    data = {
        "labels": labels,
        "counts": counts,
    }

    return JsonResponse(data)



def datasets_by_theme(request):
    """📊 Données globales : nombre de jeux de données par thème (toutes sources confondues)"""
    data = []
    for theme in Theme.objects.all():
        count = Dataset.objects.filter(themes=theme).count()
        data.append({
            "theme": theme.name,
            "count": count
        })
    return JsonResponse(data, safe=False)


def datasets_by_theme_filtered(request, source_id):
    """🎯 Données filtrées : nombre de jeux de données par thème selon la source choisie"""
    data = []
    source_datasets = Dataset.objects.filter(source_id=source_id)

    # ✅ Si la source n'a pas de thème, on attribue "Non classé"
    if not Theme.objects.filter(name="Non classé").exists():
        Theme.objects.create(name="Non classé")

    default_theme = Theme.objects.get(name="Non classé")

    for dataset in source_datasets:
        if dataset.themes.count() == 0:
            dataset.themes.add(default_theme)

    # 🔁 Maintenant on recompte normalement
    for theme in Theme.objects.all():
        count = Dataset.objects.filter(themes=theme, source_id=source_id).count()
        data.append({
            "theme": theme.name,
            "count": count
        })

    return JsonResponse(data, safe=False)


def map_view(request):
    """Affiche la carte interactive Leaflet avec les jeux de données géolocalisés"""
    datasets = Dataset.objects.exclude(latitude__isnull=True).exclude(latitude=0)

    data = [
        {
            "title": d.title,
            "description": d.description,
            "latitude": d.latitude,
            "longitude": d.longitude,
            "source": d.source.name if d.source else "Inconnue",
            "url": d.url,
        }
        for d in datasets
    ]

    # ✅ On convertit en vrai JSON ici
    return render(
    request,
    "dashboard/map.html",
    {
        "datasets_json": json.dumps(data, cls=DjangoJSONEncoder)
    },
)
