# # views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Department
from rest_framework.authtoken.models import Token
from .serializers import CustomUserSerializer, UserLoginSerializer,ChangePasswordSerializer,SendPasswordResetEmailSerializer, \
    UserPasswordResetSerializer
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, smart_str
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import update_last_login
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
import secrets
from datetime import timedelta, datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator

 
class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Call create method to save the user with hashed password
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response({"Registration has been successfully!!":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
    

class UserLoginViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Creating or updating user token
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key,'success': "Login successfully."})
  

class ChangePasswordViewSet(viewsets.GenericViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        new_password = serializer.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
    

class SendPasswordResetEmailView(viewsets.ViewSet):
    serializer_class = SendPasswordResetEmailSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=SendPasswordResetEmailSerializer)
    def create(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data, context={'token': None})
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = CustomUser.objects.get(email=email)

        # Generate a random token
        token = secrets.token_hex(20)

        # Set token expiration (e.g., 1 day)
        # expiration_date = timezone.now() + timedelta(days=1)  # Make timezone-aware
        expiration_date = timezone.now() + timedelta(minutes=3)  # Make timezone-aware

        # Save token and expiration date to user instance
        user.password_reset_token = token
        user.password_reset_token_expiration = expiration_date
        user.save()

        # Continue with the rest of your code
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        ctx = {
            'uid': uid,
            'token': token
        }
        msg_html = render_to_string('password_reset_form.html', ctx)
        plain_message = strip_tags(msg_html)

        subject = 'Your Novuscrm password request'
        recipient_list = [user.email]
        to = user.email

        send_mail(
            subject,
            plain_message,
            to,
            recipient_list,
            html_message=msg_html,
        )

        return Response({'detail': 'Password reset link sent successfully.'}, status=status.HTTP_200_OK)


class UserPasswordResetView(ViewSet):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=UserPasswordResetSerializer)
    def create(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={'uid': uid, 'token': token}
        )
        serializer.is_valid(raise_exception=True)

        # Custom password reset logic
        try:
            serializer.reset_password(uid,token)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)

 


