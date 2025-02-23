from django.contrib import admin

# Register your models here.
from . import models
admin.site.register(models.ProductWatch)
admin.site.register(models.ProductHistory)