from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project
from api.project.tasks import update_estimated_time_task

# @receiver(post_save, sender=Project)
# def update_estimated_time_on_save(sender, instance, created, **kwargs):
#     if not created:  # Only update on existing instances, not on creation
#         # Schedule the Celery task to update estimated time asynchronously
#         update_estimated_time_task.apply_async(args=[instance.id], countdown=0)