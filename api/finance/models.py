from django.db import models
from api.operation.models import operationTeam
from api.user.models import RoleMaster

# Create your models here.

class financeTeam(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)
    operation_team_data = models.ForeignKey(operationTeam, on_delete=models.CASCADE,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
     
