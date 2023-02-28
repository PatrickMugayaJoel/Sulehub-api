from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny

# local imports
from .models import StudyGroup, GroupRegistration
from apps.users.serializers import UserCreateSerializer
from core.email_service import send_email
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
            if not study_group.created_by == request.user:
                return Response({'status': False, 'message': "Permission to perform action denied"},
                                status=status.HTTP_401_UNAUTHORIZED)
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
                vdata = group_reg_serializer.validated_data
                student_regs = GroupRegistration.objects.filter(study_group=vdata['study_group'])
                students = [vdata['study_group'].created_by, ]
                for reg in student_regs:
                    if reg.is_active:
                        students.append(reg.student)
                if not request.user in students:
                    return Response({'status': False, 'message': "Permission to perform action denied"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                group_reg_serializer.save()
                data = group_reg_serializer.data
                send_email(
                    request=request, template="STUDY_GROUP_REGISTRATION",
                    recipient_list=[vdata['student'].email,], STUDY_GROUP_NAME=vdata['study_group'].name
                )
                return Response({'status': True, 'message': data}, status=status.HTTP_200_OK)
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
            if not ((study_group_reg.study_group.created_by == request.user) or (request.user == study_group_reg.student)):
                return Response({'status': False, 'message': "Permission to perform action denied"},
                                status=status.HTTP_401_UNAUTHORIZED)
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

class StudentStudyGroupRegsView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Study Groups Registration status API"

    @swagger_auto_schema(tags=["Study Groups"])
    def get(self, request, student_id=None):
        try:
            study_group_regs = GroupRegistration.objects.filter(student=int(student_id))
            filtered_regs = []
            for study_group_reg in study_group_regs: ## returning only what the user is permited to view
                if ((study_group_reg.study_group.created_by == request.user) or (request.user == study_group_reg.student)):
                    filtered_regs.append(study_group_reg)
            study_group_serializer = GroupRegistrationSerializer(filtered_regs, many=True)
            return Response({'status': True,
                             'Response': study_group_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
