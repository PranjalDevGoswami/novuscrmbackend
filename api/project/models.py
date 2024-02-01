from django.db import models
from api.operation.models  import operationTeam
from api.finance.models import financeTeam
from api.user.models import CustomUser
# Create your models here.



class Client(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    


# Project/Sales model
class Project(models.Model):
    project_id = models.CharField(max_length=100, null=True, blank=True)
    user_project_id = models.CharField(max_length=50,null=True, blank=True)
    name = models.CharField(max_length=50)
    project_type = models.CharField(max_length=100, null=True, blank=True)
    sample = models.CharField(max_length=50,null=True, blank=True)
    clients = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    cpi = models.CharField(max_length=50, null=True, blank=True)
    set_up_fee = models.CharField(max_length=50, null=True, blank=True)
    other_cost = models.CharField(max_length=50, null=True, blank=True)
    operation_team = models.ForeignKey(operationTeam, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects_as_operation_team')
    operation_select = models.BooleanField(default=False)
    finance_team = models.ForeignKey(financeTeam, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects_as_finance_team')
    finance_select = models.BooleanField(default=False)
    duration = models.DurationField(null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    

# Finance model
class finance(models.Model):
    pass    