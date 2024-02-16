from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ClientViewSet, ProjectTrackingViewSet,ProjectCBRViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'track',ProjectTrackingViewSet, basename="track")

urlpatterns = [
    path('', include(router.urls)),
    path('project_code/CBR/', ProjectCBRViewSet.as_view({'post': 'create'}), name='project-cbr'),
]