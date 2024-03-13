from rest_framework import serializers, generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,get_user_model,password_validation
from django.contrib.auth.hashers import check_password,make_password


#Country Serializer Class
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name','sub_branch','is_active']


#Language Serializer Class
class LngSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lang
        fields = ['lang_type', 'country_id', 'is_active']        
        
# Company Serializer Class
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name','entity_id','entity_name','address','country_id','is_active']

# RoleMaster Serializer Class
class RoleMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleMaster
        fields = ['name','is_active']
        
 # MenuMaster Serializer Class       
class MenuSerializer(serializers.ModelSerializer):
    role_id = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    class Meta:
        model = Menu
        fields = ['menu_name','page_link','role_id','is_active']        
        

# SubMenu Master Serializer Class        
class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submenu
        fields = ['menu', 'submenu_name','page_link','permissions','is_active']        



# Department Serializer Class

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name', 'is_active']
        
        

class CustomUserSerializer(serializers.ModelSerializer):
    user_department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'phone', 'gender', 'user_department']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        existing_user = CustomUser.objects.filter(email=value).first()
        if existing_user:
            raise serializers.ValidationError("This email address is already in use.")
        return value

    def validate(self, data):
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return data

    def create(self, validated_data):
        # Hash the password before saving it to the database
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,min_length=3)
    password = serializers.CharField(max_length=25,min_length=8, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
    

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
       
        # Check if user with this email exists
        user = CustomUser.objects.filter(email=email).first()
        
        if not user:
            raise serializers.ValidationError("User with this email does not exist.")

        if email and password:
            # If the user exists, attempt authentication
            user = authenticate(email=email, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError("Both email and password are required.")

        return data


class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        user = get_user_model().objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("User with this email does not exist.")

        if not user.check_password(old_password):
            raise serializers.ValidationError("Incorrect old password.")

        try:
            password_validation.validate_password(new_password, user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(str(e))

        data['user'] = user
        return data


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    
    def validate_email(self, value):
        user = CustomUser.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError("User with this email does not exist.")
        return value



#ZoneMaster Serializer Class

class ZoneMasterSerializer(serializers.ModelSerializer):
    zone_cities = serializers.StringRelatedField(many=True)
    regions = serializers.StringRelatedField(many=True)
    class Meta:
        model = ZoneMaster
        fields = ['name','regions', 'zone_cities','is_active']
        
# RegionMaster Serializer Class
class RegionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionMaster
        fields = ['name','zone_id','is_active']
        
# StateMaster Serializer Class

class StateMasterSerializer(serializers.ModelSerializer):
    zone_id = serializers.StringRelatedField(many=False, read_only=True)
    region_id = serializers.StringRelatedField(many=False, read_only=True)
    class Meta:
        model = StateMaster
        fields = ['name', 'zone_id','region_id','is_active']
        
        
# CityMaster Serializer Class
class CityMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityMaster
        fields = ['name','region_id','state_id','is_active']
        
        
        
                