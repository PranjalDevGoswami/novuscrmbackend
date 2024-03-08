from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ClientViewSet, ProjectTrackingViewSet, ProjectTypeListView
# ,ProjectCBRViewSet
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'track',ProjectTrackingViewSet, basename="track")

urlpatterns = [
    path('', include(router.urls)), 
    path('project_type', ProjectTypeListView.as_view()),
]