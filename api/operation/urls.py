from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AllProjectDataAPIView,OperationTeamCreateAPIView
# ,UpdateEstimateTimeAPIView,

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('projects/data', AllProjectDataAPIView.as_view(), name='get_all_project_data'),
    path('projects/estimate/', OperationTeamCreateAPIView.as_view(), name='create_operation_team'),
]
   


