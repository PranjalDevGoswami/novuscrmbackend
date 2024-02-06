from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationViewSet, UserLoginViewSet,ChangePasswordViewSet,SendPasswordResetEmailView,UserPasswordResetView


router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='user-registration')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLoginViewSet.as_view({'post': 'create'}), name='user-login'),
    path('change-password/', ChangePasswordViewSet.as_view({'post': 'create'}), name='change-password'),
    path('send_reset_password_email/', SendPasswordResetEmailView.as_view({'post': 'create'}), name='send_reset_password_email'),
    path('reset-password/<str:uid>/<str:token>/', UserPasswordResetView.as_view({'post': 'create'}), name='reset-password'),
    
]
