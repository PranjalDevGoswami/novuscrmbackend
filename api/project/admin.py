from django.contrib import admin

# Register your models here.
from .models import *



@admin.register(projectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name'] 
    list_display_links = ['id', 'name'] 

    class Meta:
        model = projectType


admin.site.register(Project)
admin.site.register(ProjectManager)
admin.site.register(Client)
admin.site.register(FeeMaster)
admin.site.register(ProjectTracking)