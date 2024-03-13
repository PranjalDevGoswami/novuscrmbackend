from django.db import models
from api.user.models import RoleMaster
from django.core.exceptions import ValidationError
from datetime import timedelta
from .choice import status_choice

# Create your models here.

class operationTeam(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)
    project_code = models.CharField(max_length=50,null=True,blank=True)
    date = models.DateTimeField(null=True,blank=True) 
    man_days = models.IntegerField(null=True,blank=True)
    total_achievement = models.CharField(max_length=255,null=True,blank=True,default=None)
    remaining_time = models.DurationField(default=timedelta(), null=True, blank=True)
    remaining_interview = models.CharField(max_length=255,null=True,blank=True,default=None)
    reason_for_adjustment = models.TextField(null=True, blank=True,default=None) 
    status = models.CharField(choices=status_choice,max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name






    




    

        


    