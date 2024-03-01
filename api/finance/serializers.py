from rest_framework import serializers
from api.user.models import RoleMaster
from .models import financeTeam
from api.project.models import Project,ProjectManager,SalesOwner,Client,FeeMaster
from api.operation.models import operationTeam
from api.operation.serializers import OperationTeamSerializer

class FinanceTeamSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(queryset=RoleMaster.objects.all(), source='role', write_only=True)
    operation_team_data = OperationTeamSerializer()
    
    class Meta:
        model = financeTeam
        fields = ['id', 'name', 'role_id', 'operation_team_data', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'operation_team_data']

    # def create(self, validated_data):
    #     role_id = validated_data.pop('role_id')
    #     validated_data['role'] = role_id
    #     return super().create(validated_data)
    


class FinanceDashboardSerializer(serializers.Serializer):
    project_id = serializers.CharField(source='project.project_id')
    name = serializers.CharField(source='project.name')
    project_type = serializers.CharField(source='project.project_type')
    sample = serializers.CharField(source='project.sample')
    cpi = serializers.CharField(source='project.cpi')
    set_up_fee = serializers.PrimaryKeyRelatedField(source='project.set_up_fee', queryset=FeeMaster.objects.all())
    other_cost = serializers.CharField(source='project.other_cost')
    tentative_end_date = serializers.DateTimeField(source='project.tentative_end_date')
    estimated_time = serializers.DurationField(source='project.estimated_time')
    operation_team = serializers.PrimaryKeyRelatedField(queryset=operationTeam.objects.all())
    finance_team = serializers.PrimaryKeyRelatedField(queryset=financeTeam.objects.all())
    operation_team_name = serializers.CharField(source='operation_team.name')
    operation_team_role = serializers.PrimaryKeyRelatedField(source='operation_team.role', queryset=RoleMaster.objects.all())
    operation_team_project_code = serializers.CharField(source='operation_team.project_code')
    operation_team_date = serializers.DateTimeField(source='operation_team.date')
    operation_team_man_days = serializers.IntegerField(source='operation_team.man_days')
    operation_team_total_achievement = serializers.CharField(source='operation_team.total_achievement')
    operation_team_remaining_time = serializers.SerializerMethodField()
    operation_team_remaining_interview = serializers.CharField(source='operation_team.remaining_interview')
    operation_team_reason_for_adjustment = serializers.CharField(source='operation_team.reason_for_adjustment')
    operation_team_status = serializers.CharField(source='operation_team.status')
    operation_team_is_active = serializers.BooleanField(source='operation_team.is_active')
    operation_team_created_at = serializers.DateTimeField(source='operation_team.created_at')
    operation_team_updated_at = serializers.DateTimeField(source='operation_team.updated_at')
    
    
    def get_operation_team_remaining_time(self, obj):
        operation_team_data = obj.get('operation_team_data')
        if operation_team_data:
            last_operation_team = operation_team_data[-1]  # Assuming the last item is the latest
            return last_operation_team.get('remaining_time', None)
        return None

