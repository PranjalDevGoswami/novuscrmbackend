from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Project)
admin.site.register(ProjectManager)
admin.site.register(Client)
admin.site.register(FeeMaster)
admin.site.register(ProjectTracking)