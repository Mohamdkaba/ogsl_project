# harvest/ckan_harvester.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from catalog.models import Dataset, Source, Organization, Theme
from asgiref.sync import sync_to_async

# ==============================================================
# 🔄 Routeur intelligent (choisit automatiquement la bonne méthode)
# ==============================================================
def harvest_ckan(source_id, query="", max_results=100):
    """Détermine automatiquement le type de source à moissonner"""
    try:
        source = Source.objects.get(id=source_id)
    except Source.DoesNotExist:
        print(f"⚠️ Source avec id={source_id} introuvable.")
        return

    name = source.name.lower()

    if "canwin" in name:
        return harvest_canwin_js(source, max_results=max_results)
    elif "boréalis" in name or "borealis" in name:
        return harvest_dataverse(source, query=query)
    else:
        return harvest_standard_ckan(source, query, max_results)


# ==============================================================
# 1️⃣ Moissonneur CKAN standard (OpenGouv, Données Québec)
# ==============================================================
def harvest_standard_ckan(source, query, max_results):
    api_url = f"{source.base_url}/api/3/action/package_search"
    total_imported = 0
    start = 0
    rows_per_page = 100

    print(f"🌐 Début de la collecte depuis {api_url} (thème='{query}') ...")

    try:
        while total_imported < max_results:
            params = {"q": query, "rows": rows_per_page, "start": start}
            response = requests.get(api_url, params=params, timeout=40)

            if response.status_code != 200:
                print(f"❌ Erreur HTTP {response.status_code} à l’appel de {api_url}")
                break

            data = response.json()
            results = data.get("result", {}).get("results", [])
            if not results:
                break

            for item in results:
                title = item.get("title", "Sans titre")
                description = item.get("notes", "")
                url = f"{source.base_url}/dataset/{item.get('name', '')}"
                publication_date = item.get("metadata_created", None)

                if publication_date:
                    try:
                        publication_date = datetime.strptime(publication_date[:10], "%Y-%m-%d").date()
                    except Exception:
                        publication_date = datetime.now().date()
                else:
                    publication_date = datetime.now().date()

                org_data = item.get("organization")
                organization = None
                if org_data:
                    organization, _ = Organization.objects.get_or_create(
                        name=org_data.get("title", "Inconnue"),
                        defaults={
                            "description": org_data.get("description", ""),
                            "website": f"{source.base_url}/organization/{org_data.get('name', '')}"
                        }
                    )

                dataset, _ = Dataset.objects.get_or_create(
                    title=title,
                    defaults={
                        "description": description,
                        "url": url,
                        "publication_date": publication_date,
                        "source": source,
                        "organization": organization,
                    },
                )

                for tag in item.get("tags", []):
                    theme_name = tag.get("display_name", "Autre")
                    theme, _ = Theme.objects.get_or_create(name=theme_name)
                    dataset.themes.add(theme)

                total_imported += 1
                if total_imported >= max_results:
                    break

            print(f"📦 {total_imported} jeux de données importés jusqu’ici depuis {source.name}...")
            start += rows_per_page

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion à {api_url} : {e}")

    print(f"✅ Collecte terminée : {total_imported} jeux de données importés depuis {source.name}.")


# ==============================================================
# 2️⃣ Moissonneur Dataverse (Boréalis)
# ==============================================================
def harvest_dataverse(source, query=""):
    print(f"🌐 Moissonnage Dataverse depuis {source.base_url} (thème='{query}') ...")
    api_url = f"{source.base_url}/api/search"
    params = {"q": query, "type": "dataset", "per_page": 100}

    try:
        response = requests.get(api_url, params=params, timeout=40)
        if response.status_code != 200:
            print(f"❌ Erreur HTTP {response.status_code} à l’appel de {api_url}")
            return

        results = response.json().get("data", {}).get("items", [])
        total_imported = 0

        org, _ = Organization.objects.get_or_create(
            name="Université du Québec à Rimouski (UQAR)",
            defaults={"description": "Institut des sciences de la mer (ISMER)"}
        )
        theme, _ = Theme.objects.get_or_create(name="Écophysiologie marine")

        for r in results:
            Dataset.objects.get_or_create(
                title=r.get("name", "Sans titre"),
                defaults={
                    "description": r.get("description", "Aucune description"),
                    "url": r.get("url", source.base_url),
                    "publication_date": datetime.now().date(),
                    "source": source,
                    "organization": org,
                },
            )
            total_imported += 1

        print(f"✅ {total_imported} jeux de données importés depuis {source.name} (Dataverse).")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion à {api_url} : {e}")


# ==============================================================
# 3️⃣ Moissonneur CanWin (Playwright — rendu JS) [VERSION SÛRE ORM]
# ==============================================================
def harvest_canwin_js(source, max_results=100):
    """
    Rend la page CanWin avec Playwright (headless), scrape les cartes,
    puis **ferme le navigateur avant** d'écrire en base.
    """
    print("🌊 Début de la collecte CanWin (rendu JS avec Playwright)...")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ Playwright n'est pas installé. Fais: pip install playwright && python -m playwright install")
        return

    base_url = "https://canwin-datahub.ad.umanitoba.ca"
    list_url = f"{base_url}/data/dataset"
    scraped = []  # <- on accumule ici les résultats (pas d'ORM pendant le scraping)

    # ——— Sélecteurs assez larges pour différents templates CKAN ———
    CARD_SELECTORS = ["div.dataset-item", "div.dataset", "div.card"]
    TITLE_SELECTORS = ["h3 a", "h2 a", "a.dataset-heading", "a[href*='/data/dataset/']"]
    DESC_SELECTORS = [".notes", ".dataset-description", "p"]

    def extract_from_html(html):
        soup = BeautifulSoup(html, "html.parser")
        # trouver des “cards”
        cards = []
        for sel in CARD_SELECTORS:
            found = soup.select(sel)
            if found:
                cards = found
                break

        for c in cards:
            # titre + lien
            a = None
            for sel in TITLE_SELECTORS:
                a = c.select_one(sel)
                if a:
                    break
            if not a:
                continue

            title = a.get_text(strip=True)
            href = a.get("href", "").strip()
            if not href:
                continue
            link = href if href.startswith("http") else (base_url + href)

            # description (facultative)
            desc = ""
            for sel in DESC_SELECTORS:
                d = c.select_one(sel)
                if d:
                    desc = d.get_text(strip=True)
                    break

            scraped.append({
                "title": title,
                "url": link,
                "description": desc or "Aucune description disponible."
            })
            if len(scraped) >= max_results:
                break

    # ——— Navigation Playwright ———
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/118.0 Safari/537.36"
            )
        )
        page = context.new_page()

        # 1) Page liste
        page.goto(list_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2000)
        extract_from_html(page.content())

        # 2) Pagination (si dispo)
        while len(scraped) < max_results:
            next_found = False
            for sel in ["a[rel='next']", "li.next a", "a.next", "a:has-text('Next')", "a:has-text('Suivant')"]:
                try:
                    loc = page.locator(sel)
                    if loc and loc.count() > 0:
                        loc.first.click()
                        page.wait_for_load_state("domcontentloaded", timeout=60000)
                        page.wait_for_timeout(1200)
                        extract_from_html(page.content())
                        next_found = True
                        break
                except Exception:
                    continue
            if not next_found:
                break

        browser.close()

    # ——— Écritures ORM **après** la fermeture du navigateur ———
    if not scraped:
        print("⚠️ Aucun jeu détecté sur CanWin (possible protection ou structure HTML différente).")
        return

    org, _ = Organization.objects.get_or_create(
        name="University of Manitoba - CanWin Data Hub",
        defaults={"description": "Plateforme canadienne des données sur le climat et l’eau."},
    )
    theme, _ = Theme.objects.get_or_create(name="Eau et climat")

    created_count = 0
    for item in scraped[:max_results]:
        dataset, created = Dataset.objects.get_or_create(
            title=item["title"],
            defaults={
                "description": item["description"],
                "url": item["url"],
                "publication_date": datetime.now().date(),
                "source": source,
                "organization": org,
            },
        )
        if created:
            dataset.themes.add(theme)
            created_count += 1

    print(f"✅ {created_count} jeux de données importés depuis CanWin (Playwright).")
