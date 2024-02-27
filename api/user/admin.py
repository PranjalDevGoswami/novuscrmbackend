from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register((CustomUser,Company,RoleMaster,RolePermission,CompanyTask,Country,CompanyDeal,Department,ZoneMaster,RegionMaster,StateMaster,CityMaster))

