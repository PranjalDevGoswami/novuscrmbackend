from django.shortcuts import render
from rest_framework import viewsets
from .models import operationTeam
from .serializers import OperationTeamSerializer
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from api.project.models import Project  
from rest_framework.decorators import api_view
from api.project.serializers import ProjectSerializer  
from .serializers import OperationTeamCreateSerializer,CBRSendToClientSerializer,ProjectPerDaySerializer  
import datetime
from django.core import signing
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError

class AllProjectDataAPIView(APIView):
    serializer_class = OperationTeamSerializer
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request):
        try:
            operation_team_ids = operationTeam.objects.values_list('id', flat=True)
            projects = Project.objects.filter(operation_team__in=operation_team_ids, status="completed")
            project_serializer = ProjectSerializer(projects, many=True)
            return Response(project_serializer.data, status=status.HTTP_200_OK)
        except operationTeam.DoesNotExist:
            return Response({"error": "OperationTeam does not exist"}, status=status.HTTP_404_NOT_FOUND)


# Assuming Project model and operationTeam model are imported
class OperationTeamCreateAPIView(APIView):
    serializer_class = OperationTeamCreateSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=OperationTeamCreateSerializer)
    def post(self, request):
        serializer = OperationTeamCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Extract project code from request data
                project_code = serializer.validated_data['project_code']
                # Check if the project exists
                try:
                    project = Project.objects.filter(project_code=project_code).first()

                except Project.DoesNotExist:
                    return Response({"error": "Project with specified project code does not exist"}, status=status.HTTP_404_NOT_FOUND)

                if project.remark == None:
                    print('**********************')
                    from django.utils.dateparse import parse_datetime

                    # Convert date strings to datetime objects
                    tentative_end_date = parse_datetime(str(project.tentative_end_date))
                    date = parse_datetime(str(serializer.validated_data.get('date')))

                    # Convert to date objects (removing time information)
                    tentative_end_date = tentative_end_date.date()
                    date = date.date()

                    # Calculate the difference in days
                    total_working_time1 = tentative_end_date - date
                  
                    # Access the days attribute to get the difference in days
                    total_working_days = total_working_time1.days
                    total_working_time = total_working_days * datetime.timedelta(hours=8)
                    
                    total_resource = serializer.validated_data.get('man_days')
                    today_working_time = total_resource * datetime.timedelta(hours=8)
                    
                    remaining_working_time = total_working_time - today_working_time
                
                    interview_sample_size = project.sample
                    interview_achievement = serializer.validated_data.get('total_achievement')
                    remaining_achievement = int(interview_sample_size) - int(interview_achievement)
                    if total_working_time and today_working_time and remaining_working_time and interview_sample_size and interview_achievement and remaining_achievement:
                        Project.objects.filter(project_code=project_code).update(remark="project_start")
                       
                else:
                    # Get last object remaining time and remaining achievement
                    print('#########################')
                    try:
                        last_operation_team = operationTeam.objects.last()
                        total_working_time = last_operation_team.remaining_time
                        total_resource = serializer.validated_data.get('man_days')
                        today_working_time = total_resource * datetime.timedelta(hours=8)
                        remaining_working_time = total_working_time - today_working_time
                        interview_sample_size = last_operation_team.remaining_interview
                        interview_achievement = serializer.validated_data.get('total_achievement')
                        remaining_achievement = int(interview_sample_size) - int(interview_achievement)
                    except Exception as e:
                        print(f"Please Send Project code and all neccessary fields: {e}")
                    
                # Create operationTeam instance
                operation_team = operationTeam.objects.create(
                    name=serializer.validated_data.get('name'),
                    role_id=1,
                    project_code=project_code,
                    date=serializer.validated_data.get('date'),
                    man_days=serializer.validated_data.get('man_days'),
                    total_achievement=serializer.validated_data.get('total_achievement'),
                    remaining_time=remaining_working_time,
                    remaining_interview = remaining_achievement,
                    reason_for_adjustment="",  # Assuming this field is always empty initially
                    status = serializer.validated_data.get('status'),
                    is_active=True,  # Assuming this field is always set to True initially
                )
              
                # Optionally, you can serialize the created object and return it in the response
                operation_team_serializer = OperationTeamSerializer(operation_team)
                return Response(operation_team_serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectCBRViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = CBRSendToClientSerializer
    permission_classes = (permissions.AllowAny,)

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
        if project.status == 'completed':
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
        
        else:
            return Response({'message': 'Please update the project status to completed. Otherwise, CBR cannot be generated.'}, status=status.HTTP_400_BAD_REQUEST)


class OperationTeamListView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProjectPerDaySerializer

    @swagger_auto_schema(request_body=ProjectPerDaySerializer)
    def post(self, request, *args, **kwargs):
        serializer = ProjectPerDaySerializer(data=request.data)
        try:
            if serializer.is_valid():
                project_code = serializer.validated_data['project_code']
                print('@@@@@@@@@@@@@@@')
                if project_code:
                    operation_teams = operationTeam.objects.filter(project_code=project_code).all()
                else:
                    operation_teams = operationTeam.objects.all()
                serializer = OperationTeamSerializer(operation_teams, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)





