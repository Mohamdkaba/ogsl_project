# portal/views.py
from django.shortcuts import render
from catalog.models import Dataset, Source, Theme, Organization
from django.core.paginator import Paginator
from random import uniform

def home(request):
    stats = {
        "sources_count": Source.objects.count(),
        "datasets_count": Dataset.objects.count(),
        "organizations_count": Organization.objects.count(),
        "themes_count": Theme.objects.count(),
    }

    sources_cards = [
        {"name": "OpenGouv", "url": "https://ouvert.canada.ca", "color": "primary"},
        {"name": "CanWin", "url": "https://canwin-datahub.ad.umanitoba.ca", "color": "success"},
        {"name": "Données Québec", "url": "https://www.donneesquebec.ca", "color": "warning"},
        {"name": "Boréalis", "url": "https://borealisdata.ca", "color": "purple"},
    ]

    # 🗺️ Simulation de coordonnées aléatoires (si manquantes)
    for dataset in Dataset.objects.filter(latitude__isnull=True)[:100]:
        dataset.latitude = uniform(45.0, 49.5)    # entre Montréal et Québec
        dataset.longitude = uniform(-79.5, -65.0)
        dataset.save()

    # 📍 Points pour l’aperçu cartographique
    points = (
        Dataset.objects.exclude(latitude__isnull=True)
        .exclude(longitude__isnull=True)
        .values("title", "description", "latitude", "longitude")[:50]
    )

    # 📦 Tous les jeux de données (pagination)
    all_datasets = Dataset.objects.order_by("-publication_date")
    paginator = Paginator(all_datasets, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "portal/home.html", {
        "stats": stats,
        "sources_cards": sources_cards,
        "page_obj": page_obj,
        "points": list(points),
    })


def search(request):
    """Recherche simple de datasets"""
    query = request.GET.get("q", "")
    results = []

    if query:
        results = Dataset.objects.filter(title__icontains=query)[:50]

    return render(request, "portal/search.html", {"query": query, "results": results})

def about(request):
    """Page à propos de l'OGSL"""
    sections = [
        {
            "title": "Contexte",
            "id": "contexte",
            "content": """L’Observatoire Global du Saint-Laurent (OGSL) a été créé pour centraliser,
            visualiser et partager les données ouvertes relatives au fleuve, à ses écosystèmes
            et à son environnement socio-économique. Le projet met à disposition des
            chercheurs, étudiants et citoyens un point d’accès unifié aux ressources
            issues de plusieurs portails officiels de données ouvertes."""
        },
        {
            "title": "Mission et vision",
            "id": "mission",
            "content": """La mission de l’OGSL est de promouvoir la transparence, la
            collaboration et la valorisation des données environnementales. Notre vision
            est celle d’un écosystème numérique ouvert où les données du Saint-Laurent
            sont accessibles, interopérables et exploitables pour l’innovation, la recherche
            et la prise de décision publique."""
        },
        {
            "title": "Concept d’observatoire",
            "id": "concept",
            "content": """L’OGSL repose sur le concept d’un observatoire numérique
            regroupant diverses sources de données (gouvernementales, municipales,
            scientifiques). Ces données sont moissonnées automatiquement, classées par
            thèmes, visualisées sur une carte et consultables via un tableau de bord
            interactif, une API REST et un endpoint GraphQL."""
        },
    ]
    return render(request, "portal/about.html", {"sections": sections})

