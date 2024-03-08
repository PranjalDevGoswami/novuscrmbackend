from rest_framework import serializers
from api.operation.models import operationTeam
from api.user.models import RoleMaster
from api.project.models import Project
class OperationTeamSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(queryset=RoleMaster.objects.all(), source='role', write_only=True)

    class Meta:
        model = operationTeam
        fields = ['id', 'name', 'role_id', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id']

    # def create(self, validated_data):
    #     role_id = validated_data.pop('role_id')
    #     validated_data['role'] = role_id
    #     return super().create(validated_data)
    

class OperationTeamCreateSerializer(serializers.ModelSerializer):
    project_code = serializers.CharField(max_length=50, write_only=True, required=True)
    date = serializers.DateTimeField(write_only=True, required=False)
    man_days = serializers.IntegerField(write_only=True, required=False)
    total_achievement = serializers.CharField(max_length=255, write_only=True, required=False, allow_blank=True)
    
    class Meta:
        model = operationTeam
        fields = ['project_code', 'date', 'man_days', 'total_achievement','status','is_active', 'created_at', 'updated_at']



class CBRSendToClientSerializer(serializers.ModelSerializer):
    project_code = serializers.CharField(max_length=50, write_only=True, required=True)
    
    class Meta:
        model = Project
        fields = ['project_code','is_active']

    def validate_project_code(self, value):
        # Check if the project code exists
        try:
            Project.objects.get(project_code=value)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Project with this code does not exist.")
        return value