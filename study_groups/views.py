from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny

# local imports
from .models import StudyGroup, GroupRegistration
from users.serializers import UserCreateSerializer
from .serializers import (
    StudyGroupSerializer, StudyGroupUpdateSerializer,
    GroupRegistrationSerializer, GroupRegistrationUpdateSerializer
)


class ListStudyGroupsView(APIView):
    permission_classes = (AllowAny,)
    __doc__ = "List all Study Groups."

    @swagger_auto_schema(tags=["Study Groups"])
    def get(self, request):
        try:
            study_groups = StudyGroup.objects.all()
            study_group_serializer = StudyGroupSerializer(study_groups, many=True)
            return Response({'status': True,
                             'Response': study_group_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class GetStudyGroupView(APIView):
    permission_classes = (AllowAny,)
    __doc__ = "GET API for Study Groups"

    @swagger_auto_schema(tags=["Study Groups"])
    def get(self, request, study_group_id=None):
        try:
            study_group = StudyGroup.objects.get(pk=int(study_group_id))
            study_group_serializer = StudyGroupSerializer(study_group, many=False)
            return Response({'status': True,
                             'Response': study_group_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class GetStudyGroupMembersView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "GET API for Study Groups Members"

    @swagger_auto_schema(tags=["Study Groups"])
    def get(self, request, study_group_id=None):
        try:
            study_group = StudyGroup.objects.get(pk=int(study_group_id))
            study_group_registrations = GroupRegistration.objects.filter(study_group=study_group)
            study_group_members = []
            for registration in study_group_registrations:
                study_group_members.append(registration.student)
            study_group_serializer = UserCreateSerializer(study_group_members, many=True)
            return Response({'status': True,
                             'Response': study_group_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class CreateStudyGroupView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Create API for Study Groups"

    @swagger_auto_schema(request_body=StudyGroupSerializer, tags=["Study Groups"])
    def post(self, request):
        try:
            study_group_serializer = StudyGroupSerializer(data=request.data)
            if study_group_serializer.is_valid():
                study_group_serializer.save()
                return Response({'status': True, 'message': study_group_serializer.data}, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in study_group_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class UpdateStudyGroupsView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Update API for Study Groups"

    @swagger_auto_schema(request_body=StudyGroupUpdateSerializer, tags=["Study Groups"])
    def put(self, request, study_group_id=None):
        try:
            study_group = StudyGroup.objects.get(pk=int(study_group_id))
            study_group_serializer = StudyGroupUpdateSerializer(study_group, data=request.data)
            if study_group_serializer.is_valid():
                study_group_serializer.save()
                return Response({'status': True, 'message': study_group_serializer.data}, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in study_group_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class JoinStudyGroupView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Study Groups Join API"

    @swagger_auto_schema(request_body=GroupRegistrationSerializer, tags=["Study Groups"])
    def post(self, request):
        try:
            group_reg_serializer = GroupRegistrationSerializer(data=request.data)
            if group_reg_serializer.is_valid():
                group_reg_serializer.save()
                return Response({'status': True, 'message': group_reg_serializer.data}, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in group_reg_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class UpdateRegistrationView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Update API for Study Groups"

    @swagger_auto_schema(request_body=GroupRegistrationUpdateSerializer, tags=["Study Groups"])
    def put(self, request, member_id=None):
        try:
            study_group_reg = GroupRegistration.objects.get(pk=int(member_id))
            study_group_reg_serializer = GroupRegistrationUpdateSerializer(study_group_reg, data=request.data)
            if study_group_reg_serializer.is_valid():
                study_group_reg_serializer.save()
                return Response({'status': True, 'message': study_group_reg_serializer.data}, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in study_group_reg_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class StudyGroupRegStatusView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Study Groups Registration status API"

    @swagger_auto_schema(tags=["Study Groups"])
    def get(self, request, student_id=None):
        try:
            study_group = GroupRegistration.objects.get(student=int(student_id))
            study_group_serializer = GroupRegistrationSerializer(study_group, many=False)
            return Response({'status': True,
                             'Response': study_group_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
