from django.db import models

class Source(models.Model):
    """Plateforme de données externe (ex : OpenGouv, CanWin, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    """Organisation ou producteur de données"""
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Theme(models.Model):
    """Catégories ou thématiques (Climat, Énergie, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Dataset(models.Model):
    """Jeu de données moissonné depuis une source CKAN"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    publication_date = models.DateField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    url = models.URLField()
    
    # Relations
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='datasets')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    themes = models.ManyToManyField(Theme, blank=True)

    # 🆕 Coordonnées géographiques pour la carte Leaflet
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title


