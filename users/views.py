from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import logout  

# Rest Framework imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView

# local imports
from .models import User
from .serializers import (
    UserCreateSerializer, 
    UserListSerializer,
    ChangePasswordSerializer,
    UserUpdateSerializer
)
from app.utils import generate_jwt_token
from core.upload_service import upload


class RegistrationAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer

    __doc__ = "Registration API for user"

    def post(self, request, *args, **kwargs):
        try:
            user_serializer = self.serializer_class(data=request.data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                data = generate_jwt_token(user, user_serializer.data)
                return Response(data, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in user_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class LoginView(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer
    
    __doc__ = "Log In API for user which returns token"

    @staticmethod
    def post(request):
        try:
            serializer = JSONWebTokenSerializer(data=request.data)
            if serializer.is_valid():
                serialized_data = serializer.validate(request.data)
                return Response({
                    'role': serialized_data['user'].role,
                    'id': serialized_data['user'].pk,
                    'token': 'JWT ' + serialized_data['token'],
                }, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                             'message': "User does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        """
        Logout API for user
        """
        try:
            user = request.user
            logout(request)
            return Response({'status': True,
                             'message': "logout successfully"},
                            status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False},
                            status=status.HTTP_400_BAD_REQUEST)

class GetUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserListSerializer
    queryset = User.objects.all()

    __doc__ = "Get User Profile"

    def get(self, request, user_id=None):
        try:
            user = self.queryset.get(pk=int(user_id))
            user_serializer = self.serializer_class(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        List all the users.
        """
        try:
            users = User.objects.all()
            user_serializer = UserListSerializer(users, many=True)

            users = user_serializer.data
            return Response({'status': True,
                             'Response': users},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class UserDPUploadView(APIView):
    permission_classes = (IsAuthenticated,)

    __doc__ = "Update user display picture"

    @staticmethod
    def post(request):
        try:
            if not request.FILES.get('file'):
                raise ObjectDoesNotExist("'Request File' object is empty")
            filepath = "uploads/pictures/profiles/" + str(request.FILES['file'])
            result = upload(request, filepath, "image")
            if result["status"]:
                request.user.DP=filepath
                request.user.save()
                return Response({'status': True,
                                'message': "image successfully uploaded",
                                'path':filepath},
                                status=status.HTTP_200_OK)
            else:
                raise Exception(result["message"])
        except Exception as e:
            return Response({'status': False,
                            'message': str(e),},
                            status=status.HTTP_400_BAD_REQUEST)

class UpdateAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    model = User
    serializer_class = UserUpdateSerializer

    __doc__ = "Profile Update API for user"

    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            user_serializer = self.serializer_class(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in user_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    __doc__ = "An endpoint for changing password."

    def update(self, request, *args, **kwargs):
        self.object = self.request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response({'status': True,
                'message': 'Password updated successfully'
                }, status=status.HTTP_200_OK
            )

        return Response({'status': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
