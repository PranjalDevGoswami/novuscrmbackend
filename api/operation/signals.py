from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import operationTeam
from api.project.models import Project
from django.db.models import Sum
from datetime import timedelta



@receiver(post_save, sender=operationTeam)
def update_project_instance(sender, instance, created, **kwargs):
    if created:
        project_code = instance.project_code
        update_project(project_code)

def update_project(project_code):
    project_instance = Project.objects.filter(project_code=project_code).first()
    if project_instance:
        # Aggregate man_days and total_achievement
        aggregation_result = operationTeam.objects.filter(project_code=project_code).aggregate(
            total_man_days=Sum('man_days'),
            total_achievement=Sum('total_achievement')
        )
        total_man_days = aggregation_result['total_man_days'] or 0
        total_achievement = aggregation_result['total_achievement'] or 0

        project_instance.man_days = total_man_days
        project_instance.total_achievement = total_achievement

        # Get the last operationTeam instance
        last_operation_team = operationTeam.objects.filter(project_code=project_code).order_by('-date').first()
        if last_operation_team:
            project_instance.remaining_interview = last_operation_team.remaining_interview
            project_instance.remaining_time = last_operation_team.remaining_time

        project_instance.save()
