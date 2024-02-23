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
    queryset = Project.objects.all()
    serializer_class = CBRSendToClientSerializer
    permission_classes = (permissions.AllowAny,)

    def send_notification_email(self, subject, template_name, recipient_list, context):
        from_email = "ankitkalinga03@outlook.com"
        msg_html = render_to_string(template_name, context)
        plain_message = strip_tags(msg_html)
        send_mail(subject, plain_message, from_email, recipient_list, html_message=msg_html)

    def handle_action(self, request, project_code, action):
        project_code = signing.loads(project_code)
        try:
            project = Project.objects.filter(project_code=project_code).first()
        except Project.DoesNotExist:
            raise NotFound("Project not found.")

        if action == 'cancelled':
            if project.status == 'cancelled':
                return Response({'message': 'Project is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
            if project.status == 'approved':
                return Response({'message': 'Project is already approved'}, status=status.HTTP_400_BAD_REQUEST)
            
            project_code = signing.dumps(project_code)
            context = {
                'project_code' : project_code
            }
            return render(request,'remarks.html', context)
        
        elif action == 'remark': 
                client_remark = request.GET.get('remarks')
                project.status = 'cancelled'
                project.remark = client_remark
                subject = 'Project Cancellation Notification'
                template_name = 'project_cancellation_email.html'
            
        elif action == 'approved':
            if project.status == 'approved':
                return Response({'message': 'Project is already approved'}, status=status.HTTP_400_BAD_REQUEST)
            if project.status == 'cancelled':
                return Response({'message': 'Project is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
            project.status = 'approved'
            subject = 'Project Approval Notification'
            template_name = 'project_approval_email.html'
            
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            clientname = project.clients.name
            purchase_order = project.clients.client_purchase_order_no
            emailid_cc = project.clients.email_id_for_cc
            additional_survey = project.clients.additional_survey
            billed_client = project.clients.total_survey_to_be_billed_to_client
            billing_instruction = project.clients.other_specific_billing_instruction
            projectname = project.name
            projectcode = project.project_code
            person_email = project.user_email
            project_manager = project.project_manager.name
        
            client_email = project.clients.email
            recipient_list = [client_email, 'finance@example.com']
            context = {
                'clientname': clientname,
                'purchase_order' : purchase_order,
                'emailid_cc' : emailid_cc, 
                'additional_survey' : additional_survey,
                'billed_client' : billed_client,
                'billing_instruction' : billing_instruction,
                'projectname': projectname,
                'projectcode' : project_code,
                'person_email':person_email,
                'project_manager':project_manager
                
            }
            self.send_notification_email(subject, template_name, recipient_list, context)
            project.save()

            return Response({'message': f'Project {action.capitalize()} and notification sent successfully'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return HttpResponse("Please press API via email button")

    def create(self, request, *args, **kwargs):
        project_code = request.data.get('project_code')
        
        if project_code is None:
            return Response({'project_code': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve the project object from the database
        try:
            project = Project.objects.filter(project_code=project_code).first()
        except Project.DoesNotExist:
            raise NotFound("Project not found.")
        
        # Check if the project status is approved
        if project.status == 'approved':
            return Response({'message': 'Project is already approved. CBR cannot be generated.'}, status=status.HTTP_400_BAD_REQUEST)
        project_code = signing.dumps(project_code)
        clientname = project.clients.name
        purchase_order = project.clients.client_purchase_order_no
        emailid_cc = project.clients.email_id_for_cc
        additional_survey = project.clients.additional_survey
        billed_client = project.clients.total_survey_to_be_billed_to_client
        billing_instruction = project.clients.other_specific_billing_instruction
        projectname = project.name
        projectcode = project.project_code
        person_email = project.user_email
        project_manager = project.project_manager.name
        
        
        # Get client email from project data
        client_email = project.clients.email

        # Send email to the client
        subject = 'Project CBR'
        recipient_list = [client_email]
        from_email = "ankitkalinga03@outlook.com"  # Replace with your sender email
        ctx = {
            'clientname': clientname,
            'purchase_order' : purchase_order,
            'emailid_cc' : emailid_cc, 
            'additional_survey' : additional_survey,
            'billed_client' : billed_client,
            'billing_instruction' : billing_instruction,
            'projectname': projectname,
            'projectcode' : project_code,
            'person_email':person_email,
            'project_manager':project_manager,
            'project' : project,
            
        }
        
        msg_html = render_to_string('cbr.html', ctx)
        plain_message = strip_tags(msg_html)
        send_mail(subject, plain_message, from_email, recipient_list,html_message=msg_html)
        
        return Response({'message': f'Project CBR sent successfully'}, status=status.HTTP_201_CREATED)
    
    def get(self, request, project_code, action):
        return self.handle_action(request, project_code, action)



    


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
