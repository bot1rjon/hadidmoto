from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Region)
admin.site.register(models.Info)
admin.site.register(models.Category)