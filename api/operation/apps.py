from django.apps import AppConfig


class OperationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.operation'
    
    # def ready(self):
    #     import operation.signals  # Import signals module
