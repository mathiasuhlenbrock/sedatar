from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Database)
admin.site.register(models.Post)
admin.site.register(models.Search)