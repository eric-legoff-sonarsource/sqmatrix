from django.contrib import admin
from .models import Sonarqube, Plugin, Compatibility

# Register your models here.
admin.site.register(Sonarqube)
admin.site.register(Plugin)
admin.site.register(Compatibility)
