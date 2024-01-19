from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from novuscrm.api.user.choice import lang_choice
# Create your models here.


# Country model
class Country(models.Model):
    name = models.CharField(max_length=100)
    sub_branch = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Language model
class Lang(models.Model):
    lang_type = models.CharField(choices=lang_choice)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.lang_type
    


# company model
class Company(models.Model):
    name = models.CharField(max_length=150)
    entity_id = models.CharField(max_length=50)
    entity_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    country_id = models.ForeignKey(Country, on_delete = models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    


# RoleMaster model
class RoleMaster(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


# RoleAssignment model
class RoleAssignment(models.Model):
    is_edit = models.BooleanField(default=False)
    is_view = models.BooleanField(default=False)
    is_create = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

        
    




# CustomUser model
class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, default='Anonymous')
    email = models.EmailField(max_length=100, unique=True) 
    username = None  
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    company = models.ForeignKey(Company , on_delete=models.CASCADE, null=True, blank=True)
    user_role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    



# ZoneMaster model
class ZoneMaster(models.Model):
    name = models.CharField(max_length=50)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    



# RegionMaster model
class RegionMaster(models.Model):
    name = models.CharField(max_length=50)
    zone_id = models.ForeignKey(ZoneMaster, on_delete=models.CASCADE, null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

# StateMaster model
class StateMaster(models.Model):
    name = models.CharField(max_length=50)
    zone_id = models.ForeignKey(ZoneMaster, on_delete=models.CASCADE, null=True,blank=True)
    region_id = models.ForeignKey(RegionMaster, on_delete=models.CASCADE, null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

# CityMaster model
class CityMaster(models.Model):
    name = models.CharField(max_length=50)
    zone_id = models.ForeignKey(ZoneMaster, on_delete=models.CASCADE, null=True,blank=True)
    region_id = models.ForeignKey(RegionMaster, on_delete=models.CASCADE, null=True,blank=True)
    state_id = models.ForeignKey(StateMaster, on_delete=models.CASCADE, null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


