from rest_framework import serializers
from .models import Project
from api.finance.serializers import FinanceTeamSerializer
from api.operation.serializers import OperationTeamSerializer
from api.finance.models import financeTeam
from api.operation.models import operationTeam




class ProjectSerializer(serializers.ModelSerializer):
    operation_team = serializers.StringRelatedField(many=False, read_only=True)
    finance_team = serializers.StringRelatedField(many=False,required=False)
    
    # operation_team = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name="operation-detail")
    # finance_team = serializers.HyperlinkedRelatedField(many=False,read_only=True,  view_name="finance-detail")

    class Meta:
        model = Project
        fields = ['id','name','project_type','sample','cpi','clients','set_up_fee','other_cost','operation_team','operation_select','finance_team','finance_select','duration','is_active']

    def create(self, validated_data):
        operation_team_data = validated_data.pop('operation_team', None)
        finance_team_data = validated_data.pop('finance_team', None)

        project = Project.objects.create(**validated_data)

        if operation_team_data and validated_data.get('operation_select', False):
            role = "YourOperationRole"  # Replace with the actual role for operation team members
            operation_team = operationTeam.objects.create(project=project, role=role, **operation_team_data)
            project.operation_team = operation_team
            project.save()

        if finance_team_data and validated_data.get('finance_select', False):
            role = "YourFinanceRole"  # Replace with the actual role for finance team members
            finance_team = financeTeam.objects.create(project=project, role=role, **finance_team_data)
            project.finance_team = finance_team
            project.save()

        return project