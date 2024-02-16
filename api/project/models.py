from django.db import models
from api.operation.models  import operationTeam
from api.finance.models import financeTeam
from api.user.models import CustomUser
from django.core.exceptions import ValidationError
from datetime import date , datetime
from .ch import project_choice

# Create your models here.


# CustomProjectManager Table
class CustomProjectManager(models.Manager):
    def create(self, validated_data):
        # Perform custom validation here
        if validated_data['tentative_end_date'] < date.today():
            raise ValidationError("Tentative end date cannot be in the past.")
        
        if self.duration and self.duration.total_seconds() <= 0:
            raise ValidationError({'duration': ['Duration must be greater than 0.']})

        return super().create(validated_data)
    
    
    
# Client Master Table
class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# FeeMaster Model table
class FeeMaster(models.Model):
    fee_type = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=8, decimal_places=2) 
    is_default = models.BooleanField(default=True)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.fee_type
    
# ProjectManager Model table
class ProjectManager(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    is_active = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    


# Project/Sales model
class Project(models.Model):
    project_id = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    user_email = models.EmailField(max_length=255,null=True,blank=True)
    project_manager = models.ForeignKey(ProjectManager,on_delete=models.CASCADE,null=True,blank=True,related_name="projects_manager")
    project_code = models.CharField(max_length=50,null=True,blank=True)
    name = models.CharField(max_length=50)
    project_type = models.CharField(choices=project_choice,max_length=100, null=True, blank=True)
    sample = models.CharField(max_length=50,null=True, blank=True)
    clients = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    cpi = models.CharField(max_length=50, null=True, blank=True)
    set_up_fee = models.ForeignKey(FeeMaster, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects_fee")
    other_cost = models.CharField(max_length=50, null=True, blank=True)
    operation_team = models.ForeignKey(operationTeam, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects_as_operation_team')
    operation_select = models.BooleanField(default=False)
    finance_team = models.ForeignKey(financeTeam, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects_as_finance_team')
    finance_select = models.BooleanField(default=False)
    tentative_start_date = models.DateTimeField(null=True,blank=True)
    tentative_end_date = models.DateTimeField(null=True,blank=True)
    estimated_time = models.DurationField(null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    # updated estimated time 
    def save(self, *args, **kwargs):
        if self.tentative_start_date and self.tentative_end_date:
            self.estimated_time = self.tentative_end_date - self.tentative_start_date

        super().save(*args, **kwargs)
    
class ProjectTracking(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    durations = models.DurationField()
    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.project.name
    
    

# Finance model
class finance(models.Model):
    pass    