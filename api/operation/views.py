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
from .serializers import OperationTeamCreateSerializer  
import datetime

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
                print(project_code,'DFFFFFFFFFFF')
                # Check if the project exists
                try:
                    project = Project.objects.get(project_code=project_code)
                    print(project,'HHHHHHHHHHHHH')
                except Project.DoesNotExist:
                    return Response({"error": "Project with specified project code does not exist"}, status=status.HTTP_404_NOT_FOUND)

                if project.remark == None:
                    Project.objects.filter(project_code=project_code).update(remark="project_start")
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
                    total_working_time = total_working_days * 8
                    
                    total_resource = serializer.validated_data.get('man_days')
                    today_working_time = total_resource * 8
                    
                    remaining_working_time = total_working_time - today_working_time
                    
                    interview_sample_size = project.sample
                    interview_achievement = serializer.validated_data.get('total_achievement')
                    remaining_achievement = int(interview_sample_size) - int(interview_achievement)
                    
                else:
                    # Get last object remaining time and remaining achievement
                    print('#########################')
                    last_operation_team = operationTeam.objects.last()
                    total_working_time = last_operation_team.remaining_time
                    total_resource = serializer.validated_data.get('man_days')
                    today_working_time = total_resource * datetime.timedelta(hours=8)
                    remaining_working_time = total_working_time - today_working_time
                    interview_sample_size = last_operation_team.remaining_interview
                    interview_achievement = serializer.validated_data.get('total_achievement')
                    remaining_achievement = int(interview_sample_size)- int(interview_achievement)

                # Create operationTeam instance
                operation_team = operationTeam.objects.create(
                    name="operationTeam1",
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






