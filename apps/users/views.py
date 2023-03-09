from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import logout

# Rest Framework imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from drf_yasg.utils import swagger_auto_schema
import json
from apps.utils import JsonEncoder
from django.core import serializers

# local imports
from .models import User
from .serializers import (
    UserCreateSerializer, 
    UserListSerializer,
    ChangePasswordSerializer,
    UserUpdateSerializer
)
from core.upload_service import upload
from core.email_service import send_email
from apps.events.models import Invitation
from apps.events.serializers import InvitationSerializer, InvitationCreateSerializer, InviteUpdateSerializer


class AddUserAPIView(APIView):
    # authentication_classes = []
    permission_classes = (AllowAny,)

    __doc__ = "Registration API for user"

    @swagger_auto_schema(tags=["Users"], request_body=UserCreateSerializer)
    def post(self, request, *args, **kwargs):
        try:
            user_serializer = UserCreateSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                data = user_serializer.data
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

class InvitationsCreateView(APIView):
    
    __doc__ = "User Invitation API"

    @staticmethod
    @swagger_auto_schema(request_body=InvitationCreateSerializer, tags=["Users"])
    def post(request):
        try:
            invitation_serializer = InvitationSerializer(data=request.data)
            if invitation_serializer.is_valid():
                invitation = invitation_serializer.save()
                send_email(
                    request=request,
                    template="INVITE_A_USER",
                    SCHOOL_NAME=invitation.school.name,
                    INVITE_ID=invitation.id,
                    USER_TYPE=invitation.user_type,
                    recipient_list=[invitation.email,]
                )
                return Response({
                    'message': "Invitation successfully sent.",
                }, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in invitation_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False, 'message': message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'status': False,'message': "Error sending Invitation!"},
                            status=status.HTTP_400_BAD_REQUEST)

class GetInvitationView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "GET API for invitation"

    @swagger_auto_schema(tags=["Users"])
    def get(self, request, invite_id=0):
        try:
            invites = Invitation.objects.get(pk=int(invite_id))
            data = json.loads(serializers.serialize('json', [invites,], use_natural_foreign_keys=True, cls=JsonEncoder))[0]
            return Response({'status': True, 'Response': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateInvitationView(APIView):
    permission_classes = (IsAuthenticated,)

    __doc__ = "Invitation Update view"

    @swagger_auto_schema(tags=["Users"], request_body=InviteUpdateSerializer)
    def put(self, request, invite_id=0):
        try:
            invite = Invitation.objects.get(pk=int(invite_id))
            if isinstance(request.data.get("is_active"), bool):
                invite.is_active = request.data.get("is_active")
                invite.save()
                data = json.loads(serializers.serialize('json', [invite,], use_natural_foreign_keys=True, cls=JsonEncoder))[0]
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'status': False, 'message': "invalid input!"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class GetUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserListSerializer

    __doc__ = "Get User by id"

    @swagger_auto_schema(tags=["Users"])
    def get(self, request, user_id=0):
        try:
            user = User.objects.get(pk=int(user_id))
            user_serializer = self.serializer_class(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class GetUserEmailView(APIView):
    permission_classes = (IsAuthenticated,)

    __doc__ = "Get User email"

    @swagger_auto_schema(tags=["Users"])
    def get(self, request, email=None):
        try:
            user = User.objects.get(email=email)
            user_serializer = UserListSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(tags=["Users"])
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

    @swagger_auto_schema(tags=["Users"])
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

class UpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    model = User

    __doc__ = "Profile Update API for user"

    @swagger_auto_schema(tags=["Users"], request_body=UserUpdateSerializer)
    def put(self, request, *args, **kwargs):
        try:
            user = self.request.user
            user_serializer = UserUpdateSerializer(user, data=request.data)
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

class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    __doc__ = "An endpoint for changing password."

    @swagger_auto_schema(tags=["Users"], request_body=ChangePasswordSerializer)
    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()

            return Response({'status': True,
                'message': 'Password updated successfully'
                }, status=status.HTTP_200_OK
            )

        return Response({'status': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
