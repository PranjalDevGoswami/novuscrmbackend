from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from api.user import views


router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='user-registration')
router.register(r'zone', ZoneViewSet,basename='zone')
router.register(r'region', RegionViewSet,basename='region')
router.register(r'city', CityViewSet,basename='city')



urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLoginViewSet.as_view({'post': 'create'}), name='user-login'),
    path('api/users-list/', UserLists.as_view(), name='user-list'),
    path('change-password/', ChangePasswordViewSet.as_view({'post': 'create'}), name='change-password'),
    path('reset-password/', ResetPasswordViewSet.as_view({'post': 'create'}), name='reset-password'),
    # path('cites/', views.CityList.as_view()),
  
]

