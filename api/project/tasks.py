# tasks.py
from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Project

# @shared_task(bind=True, queue='celery')
# def update_estimated_time_task(self,project_id):
#     try:
#         project = Project.objects.get(id=project_id)
#         if project.tentative_start_date and project.tentative_end_date:
#             current_date = timezone.now().date()
#             end_date = project.tentative_end_date.date()
#             print("current_date", current_date)
#             print("end_date", end_date)
#             days_difference = (end_date - current_date).days
#             print("days_difference", days_difference)
#             project.estimated_time = max(timedelta(days=days_difference), timedelta(0))
#             project.save()
#             print("Time Update Successfully !!")
#     except Project.DoesNotExist:
#         print(f"Project with ID {project} does not exist.")
#         return f"Project with ID {project} does not exist."
    
#     return f"Estimated time updated for project {project_id}."


from django.core.cache import cache
from datetime import date

@shared_task(bind=True)
def update_estimated_time_task(self):
    # Check if the task has already run today
    last_run_date = cache.get('last_run_date')
    if last_run_date == date.today():
        print("Task already ran today. Skipping.")
        return "Task already ran today. Skipping."

    try:
        projects = Project.objects.all()
        for project in projects:
            if project.tentative_start_date and project.tentative_end_date:
                current_date = timezone.now().date()
                end_date = project.tentative_end_date.date()
                days_difference = (end_date - current_date).days
                project.estimated_time = max(timedelta(days=days_difference), timedelta(0))
                project.save()
    except Project.DoesNotExist:
        print(f"Project with ID {project} does not exist.")
        return f"Project with ID {project} does not exist."

    # Update the last run date to today
    cache.set('last_run_date', date.today())

    return f"Estimated time updated for project."

# @shared_task(bind=True)
# def update_estimated_time_task(self, *args, **kwargs):
#     try:
#         # Fetch the project ID dynamically, e.g., from the kwargs
#         project_id = kwargs.get('project_id')
        
#         if project_id is not None:
#             project = Project.objects.get(id=project_id)
#             if project.tentative_start_date and project.tentative_end_date:
#                 current_date = timezone.now().date()
#                 end_date = project.tentative_end_date.date()
#                 days_difference = (end_date - current_date).days
#                 project.estimated_time = max(timedelta(days=days_difference), timedelta(0))
#                 project.save()
#         else:
#             print("No project ID provided.")
#     except Project.DoesNotExist:
#         print(f"Project with ID {project_id} does not exist.")
        

# @shared_task(bind=True)
# def update_estimated_time_task(self, project_id):
#     project = Project.objects.get(id=project_id)
#     if project.tentative_start_date and project.tentative_end_date:
#         current_date = timezone.now().date()
#         days_difference = (project.tentative_end_date - current_date).days - 1
#         project.estimated_time = max(timedelta(days=days_difference), timedelta(0))
#         project.save()
        
# @shared_task(bind=True)
# def update_estimated_time_task(self, project_id):
#     try:
#         project = Project.objects.get(id=project_id)
#         if project.tentative_start_date and project.tentative_end_date:
#             # Convert project.tentative_end_date to datetime if it's a date object
#             end_date = project.tentative_end_date
#             if isinstance(project.tentative_end_date, timezone.datetime):
#                 end_date = project.tentative_end_date
#             else:
#                 end_date = timezone.datetime.combine(project.tentative_end_date, timezone.datetime.min.time())

#             current_date = timezone.now().date()
#             days_difference = (end_date - current_date).days - 1
#             project.estimated_time = max(timedelta(days=days_difference), timedelta(0))
#             project.save()
#     except Project.DoesNotExist:
#         # Handle the case where the project does not exist
#         pass        


# @shared_task(bind=True)
# def update_estimated_time_task(self, project_id):
#     try:
#         project = Project.objects.get(id=project_id)

#         # Ensure consistent date comparison by extracting dates
#         current_date = timezone.now().date()
#         end_date = project.tentative_end_date.date()  # Extract date from datetime

#         # Handle cases where tentative_end_date is in the past or equal to current_date
#         days_difference = max(end_date - current_date, timedelta(0)).days - 1

#         # Ensure estimated_time is always a positive timedelta
#         project.estimated_time = max(timedelta(days=days_difference), timedelta(0))
#         project.save()

#     except Project.DoesNotExist:
#         # Log a warning or handle appropriately
#         self.retry(countdown=60)  # Retry after a minute in case of temporary issue

