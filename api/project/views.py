from rest_framework import viewsets
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .models import *
from .serializers import *
from api.finance.models import financeTeam
from api.operation.models import operationTeam
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.exceptions import NotFound
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.template.defaultfilters import linebreaksbr
from rest_framework import viewsets, permissions, status
from django.core import signing
from django.shortcuts import render

def validate_user_session(id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        if user.id == id:
            return True
        return False
    except UserModel.DoesNotExist:
        return False    
    


class ProjectTypeListView(APIView):
     
    def get(self, request, format=None):
        projects = projectType.objects.all()
        serializer = ProjectTypeSerializer(projects, many=True)
        return Response(serializer.data)



class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (permissions.AllowAny,)
    
    @swagger_auto_schema(request_body=ClientSerializer)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=ProjectSerializer)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    
    
    @swagger_auto_schema(request_body=ProjectSerializer)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        # Your custom logic for updating estimate_time here
        tentative_start_date = serializer.validated_data.get('tentative_start_date')
        tentative_end_date = serializer.validated_data.get('tentative_end_date')

        if tentative_start_date and tentative_end_date:
            duration = tentative_end_date - tentative_start_date
            estimate_time = duration.days

            if estimate_time <= 1:
                raise serializers.ValidationError("Your estimate goes to finish, please complete your task as priorities.")
        self.perform_update(serializer)
        return Response(serializer.data)
    
    
    @swagger_auto_schema(request_body=ProjectSerializer)
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Custom logic for updating estimate_time
        self.validate_and_update_estimate_time(serializer)

        self.perform_update(serializer)
        return Response(serializer.data)
    
    
    @swagger_auto_schema()
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class ProjectTrackingViewSet(viewsets.ModelViewSet):
    queryset = ProjectTracking.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (permissions.AllowAny,)
    
    @swagger_auto_schema(request_body=ClientSerializer)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
