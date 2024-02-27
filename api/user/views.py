# # views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .models import *
from rest_framework.authtoken.models import Token
from .serializers import *
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import update_last_login
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'snippets': reverse('snippet-list', request=request, format=format)
    })


#Country ViewSet
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (permissions.AllowAny,)
    

    
    

# User RegistrationViewset    
class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Call create method to save the user with hashed password
        ''' perform create method is used to add extra information when creating a new object. 
        perform_create() method will not execute if you override create() method.'''
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    

class UserLists(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializers
    queryset = CustomUser.objects.all()
    
    @swagger_auto_schema(
        operation_description="Return a list of all users.",
        responses={200: UserSerializers(many=True)},
        )
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        users = CustomUser.objects.all()
        serialized_users = UserSerializers(users, many=True).data
        return JsonResponse({'users': serialized_users}, safe=False)
    
    
class UserLoginViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Creating or updating user token
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key,'success': "Login successfully."})

@csrf_exempt
def signOut(request, id):
    logout(request)
    UserModel = get_user_model()
    
    try:
        user = CustomUser.objects.get(pk=id)
        print(user)
        user.session_token="0"
        user.save()
    except UserModel.DoesNotExist:
        return JsonResponse({"error":"Invalid User ID"}) 
    
    return JsonResponse({"success":"Logout success"})   


class ChangePasswordViewSet(viewsets.GenericViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        new_password = serializer.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
    
    



class ResetPasswordViewSet(viewsets.ViewSet):
    serializer_class = ResetPasswordSerializer
    permission_classes = (permissions.AllowAny,)
    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    
    def create(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = CustomUser.objects.get(email=email)

        # Generate a password reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Generate the reset link
        # reset_link = f"http://127.0.0.1:8000/api/user/reset-password/{uid}/{token}/"  # Replace with your actual domain

        # Render the HTML email content
        ctx = {
            'uid': uid,
            'token':token
                }
        
        msg_html = render_to_string('password_reset_form.html', ctx)
        plain_message = strip_tags(msg_html)

        # Send the password reset email
        subject = 'Your Novuscrm password request'
        recipient_list = [user.email] 
        to = user.email
        print('89877878',to)
        # to = "ankitkalinga03@outlook.com"
        send_mail(
            subject,
            plain_message,
            to,
            recipient_list,
            html_message=msg_html,
        )

        # Update last login to mark the user as active
        update_last_login(None, user)

        return Response({'detail': 'Password reset link sent successfully.'}, status=status.HTTP_200_OK)





# class CityList(APIView):
#     def get(self, request, format=None):
#         cites = CityMaster.objects.all()
#         serializer = CityMasterSerializer(cites, many=False)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CityMasterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = ZoneMaster.objects.all()
    serializer_class = ZoneMasterSerializer
    permission_classes = (permissions.AllowAny,)  
    


class RegionViewSet(viewsets.ModelViewSet):
    queryset = RegionMaster.objects.all()
    serializer_class = RegionMasterSerializer
    permission_classes = (permissions.AllowAny,)      
    
    
class CityViewSet(viewsets.ModelViewSet):
    queryset = CityMaster.objects.all()
    serializer_class = CityMasterSerializer
    permission_classes = (permissions.AllowAny,)    