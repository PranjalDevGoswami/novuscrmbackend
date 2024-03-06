from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.project.models import Project
from .serializers import FinanceDashboardSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from django.core import signing
from .models import financeTeam
from .serializers import FinanceTeamSerializer


class AllFinanceTeamDataAPIView(APIView):
    serializer_class = FinanceTeamSerializer
    permission_classes = (permissions.AllowAny,)  # Adjust permissions as needed
    
    def get(self, request):
        try:
            finance_teams = financeTeam.objects.all()
            finance_team_data = []
            for finance_team in finance_teams:
                finance_team_serializer = FinanceTeamSerializer(finance_team)
                finance_team_data.append({
                    'finance_team': finance_team_serializer.data,
                     'project_code': self.get_projects(finance_team) # Fetch associated projects
                })
            return Response(finance_team_data, status=status.HTTP_200_OK)
        except financeTeam.DoesNotExist:
            return Response({"error": "FinanceTeam does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    def get_projects(self, finance_team):
        try:
            return Project.objects.filter(operation_team=finance_team.operation_team_data, status="completed").values_list('project_code', flat=True)
        except Project.DoesNotExist:
            return []


class FinanceDashboardAPIView(APIView):
    serializer_class = FinanceDashboardSerializer
    permission_classes = (permissions.AllowAny,)
    def get(self, request, project_code):
        try:
            project = Project.objects.filter(project_code=project_code).first()
            serializer = FinanceDashboardSerializer({
                'project': project,
                'operation_team': project.operation_team,
                'finance_team': project.finance_team
            })
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"error": "Project with specified project code does not exist"}, status=status.HTTP_404_NOT_FOUND)