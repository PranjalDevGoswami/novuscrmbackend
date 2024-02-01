from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from api.user.choice import lang_choice,gender_choice
from .managers import CustomUserManager
# Create your models here.
# from api.finance import financeTeam
# from api.operation import operationTeam

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
    lang_type = models.CharField(choices=lang_choice,max_length=100)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.lang_type
    


# Company model
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

# Company Deal  
class CompanyDeal(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    close_date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
# Company task
class CompanyTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    company_deal = models.ForeignKey(CompanyDeal, on_delete=models.CASCADE, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


# RoleMaster model
class RoleMaster(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
    
# Menu Master Table    
class Menu(models.Model):
    menu_name = models.CharField(max_length=255)
    page_link = models.CharField(max_length=255)
    role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# SubMenu Master table
class Submenu(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    submenu_name = models.CharField(max_length=255)
    page_link = models.CharField(max_length=255)
    permissions = models.ManyToManyField("auth.Permission")   
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    

# Department model
class Department(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    


# RolePermission model
class RolePermission(models.Model):
    is_edit = models.BooleanField(default=False)
    is_view = models.BooleanField(default=False)
    is_create = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
 
        

# CustomUser model
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True) 
    username = models.CharField(max_length=150, blank=True, null=True, default='Anonymous')
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(choices=gender_choice,max_length=20, null=True, blank=True)
    company = models.ForeignKey(Company , on_delete=models.CASCADE, null=True, blank=True)
    user_role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE, null=True, blank=True)
    user_department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    user_permission = models.ForeignKey(RolePermission, on_delete=models.CASCADE, null=True, blank=True)
    user_company_task = models.ForeignKey(CompanyTask, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = CustomUserManager()
    
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
    

# ROle Assignment Model
# class RoleAssignment(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
#     roles = models.ForeignKey(RoleMaster, on_delete=models.CASCADE,null=True, blank=True)
#     zones = models.ManyToManyField(ZoneMaster, null=True, blank=True)
#     regions = models.ManyToManyField(RegionMaster, null=True, blank=True)
#     states = models.ManyToManyField(StateMaster, null=True, blank=True)
#     city = models.ManyToManyField(StateMaster, null=True, blank=True) 
#     is_create = models.BooleanField(default=False)
#     is_edit = models.BooleanField(default=False)
#     is_view = models.BooleanField(default=False)
#     created_on = models.DateTimeField(auto_now=True)
#     updated_on = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username
    
