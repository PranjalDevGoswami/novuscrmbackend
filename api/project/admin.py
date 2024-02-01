from django.contrib import admin

# Register your models here.
from .models import Project , Client

admin.site.register(Project)
admin.site.register(Client)