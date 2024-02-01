from rest_framework import serializers
from api.operation.models import operationTeam
from api.user.models import RoleMaster
class OperationTeamSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(queryset=RoleMaster.objects.all(), source='role', write_only=True)

    class Meta:
        model = operationTeam
        fields = ['id', 'name', 'role_id', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id']

    def create(self, validated_data):
        role_id = validated_data.pop('role_id')
        validated_data['role'] = role_id
        return super().create(validated_data)