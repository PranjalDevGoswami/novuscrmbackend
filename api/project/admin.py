from django.contrib import admin

# Register your models here.
from .models import Project , Client, FeeMaster, ProjectTracking

admin.site.register(Project)
admin.site.register(Client)
admin.site.register(FeeMaster)
admin.site.register(ProjectTracking)