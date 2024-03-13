from rest_framework import serializers
from .models import Project, Client, ProjectTracking
from api.finance.serializers import FinanceTeamSerializer
from api.operation.serializers import OperationTeamSerializer
from api.finance.models import financeTeam
from api.operation.models import operationTeam
from datetime import datetime, date



class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name','is_active']



class ProjectSerializer(serializers.ModelSerializer):
    operation_team = serializers.StringRelatedField(many=False, read_only=True)
    finance_team = serializers.StringRelatedField(many=False,required=False)
   
    def create(self, validated_data):
        # tentative_end_date should not be less than present date 
        tentative_end_date = validated_data.get('tentative_end_date')
        
        if tentative_end_date and tentative_end_date.date() < date.today():
            raise serializers.ValidationError("Tentative end date cannot be in the past.")
        
        return super().create(validated_data)

    # operation_team = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name="operation-detail")
    # finance_team = serializers.HyperlinkedRelatedField(many=False,read_only=True,  view_name="finance-detail")
         
    class Meta:
        model = Project
        fields = ['id','name','user_id','project_type','project_code','man_days','total_achievement','remaining_time','remaining_interview','user_email','project_manager','sample','cpi','clients','set_up_fee','other_cost','operation_team','operation_select','finance_team','finance_select','tentative_start_date','tentative_end_date','estimated_time','status','is_active']

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['project_type'] = {'id': instance.project_type.id,'name': instance.project_type.name} if instance.project_type else None
    #     data['clients'] = {'id': instance.clients.id,'name': instance.clients.name} if instance.clients else None
    #     return data
        
class ProjectTrackingSerializer(serializers.ModelSerializer):
    projects = serializers.StringRelatedField(many=True, read_only=True)
    users = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = ProjectTracking
        fields = ['projects','users','start_date','end_date','durations']