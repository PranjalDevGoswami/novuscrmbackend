from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationViewSet, UserLoginViewSet,ChangePasswordViewSet,ResetPasswordViewSet


router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='user-registration')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLoginViewSet.as_view({'post': 'create'}), name='user-login'),
    path('change-password/', ChangePasswordViewSet.as_view({'post': 'create'}), name='change-password'),
    path('reset-password/', ResetPasswordViewSet.as_view({'post': 'create'}), name='reset-password'),
]
