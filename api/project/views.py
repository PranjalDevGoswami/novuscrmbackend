from rest_framework import viewsets
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .models import Project, Client, ProjectTracking
from .serializers import ProjectSerializer, ClientSerializer,ProjectTrackingSerializer,CBRSendToClientSerializer
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


def validate_user_session(id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        if user.id == id:
            return True
        return False
    except UserModel.DoesNotExist:
        return False    
    

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
    


class ProjectCBRViewSet(viewsets.ModelViewSet):
    # queryset = Project.objects.all()
    serializer_class = CBRSendToClientSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=CBRSendToClientSerializer)
    def create(self, request, *args, **kwargs):
        project_code = request.data.get('project_code')
        
        if project_code is None:
            return Response({'project_code': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve the project object from the database
        try:
            project = Project.objects.filter(project_code=project_code).first()
        except Project.DoesNotExist:
            raise NotFound("Project not found.")
        except Project.MultipleObjectsReturned:
            project = Project.objects.filter(project_code=project_code).order_by('pk').first()
        
        
        clientname = f"Name of Client: {project.clients.name}"
        projectname = f"Project Name: {project.name}"
        projectcode = f"Project Code: {project.project_code}"
        person_email = f"Client Contact Person Email Address: {project.user_email}"
        project_manager = f"Project Manager Name: {project.project_manager.name}"

        
        

        # Get client email from project data
        client_email = project.clients.email
        # Send email to the client
        subject = 'Project CBR'
        recipient_list = [client_email]
        from_email = "ankitkalinga03@outlook.com"  # Replace with your sender email
        ctx = {
            'uid': "uid",
            'token':"token",
            'clientname': clientname,
            'projectname': projectname,
            'projectcode' : projectcode,
            'person_email':person_email,
            'project_manager':project_manager
            
                }
        msg_html = render_to_string('cbr.html', ctx)
        plain_message = strip_tags(msg_html)
        send_mail(subject, plain_message, from_email, recipient_list,html_message=msg_html)
         
        
        return Response(status=201, headers={'messages':'cbr genrate successfully'})
    
    


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
