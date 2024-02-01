from rest_framework import viewsets
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer
from api.finance.models import financeTeam
from api.operation.models import operationTeam
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions


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
    
    
    @swagger_auto_schema()
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        operation_team_data = serializer.validated_data.get('operation_team')
        finance_team_data = serializer.validated_data.get('finance_team')

        project = serializer.save()

        if operation_team_data and serializer.validated_data.get('operation_select', False):
            role = "YourOperationRole"  # Replace with the actual role for operation team members
            operation_team = project.operation_team.create(role=role, **operation_team_data)

        if finance_team_data and serializer.validated_data.get('finance_select', False):
            finance_team_data['role_id'] = serializer.validated_data.get('finance_team', {}).get('role_id')
            finance_team = project.finance_team.create(**finance_team_data)

    def get_serializer(self, *args, **kwargs):
        if 'data' in kwargs:
            data = kwargs['data']
            if isinstance(data, list):
                kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)
    
    