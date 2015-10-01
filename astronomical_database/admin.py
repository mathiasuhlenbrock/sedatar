from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Catalogue)
admin.site.register(models.Category)
admin.site.register(models.Planet)
admin.site.register(models.PlanetarySystem)
admin.site.register(models.Post)
