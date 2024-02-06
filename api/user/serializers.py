from rest_framework import serializers, generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Department
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,get_user_model,password_validation
from django.contrib.auth.hashers import check_password,make_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone


class CustomUserSerializer(serializers.ModelSerializer):
    user_department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone', 'gender', 'user_department']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        existing_user = CustomUser.objects.filter(email=value).first()
        if existing_user:
            raise serializers.ValidationError("This email address is already in use.")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

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


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    
    def validate_email(self, value):
        user = CustomUser.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        error_msg = "Passwords do not match."
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(error_msg)
        return attrs

    def reset_password(self, uid, token):
        try:
            uid_str = smart_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(id=uid_str)

            # Check if token is valid and not expired
            if user.password_reset_token != token or timezone.now() > user.password_reset_token_expiration:
                raise serializers.ValidationError('Token is not valid or expired')

            # Set new password
            user.set_password(self.validated_data['password'])
            user.save()

            return user
        except DjangoValidationError:
            raise serializers.ValidationError('Token is not valid or expired')







