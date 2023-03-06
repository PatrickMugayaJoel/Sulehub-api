from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from apps.users.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
from apps.utils import JsonEncoder
from django.core import serializers

# local imports
from .models import Subject , TeacherRegistration, StudentRegistration
from .serializers import (
        SubjectSerializer,
        SubjectUpdateSerializer,
        TeachersSerializer,
        TeachersUpdateSerializer,
        StudentsSerializer,
        StudentsUpdateSerializer
)


#############################################
## Subjects
#############################################
class ListSubjectsView(APIView):
    serializer_class = SubjectSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(tags=["Subjects"])
    def get(self, request, school_id):
        __doc__ = "List all subjects."
        try:
            subjects = Subject.objects.filter(school__school_id=school_id)
            subject_serializer = self.serializer_class(subjects, many=True)
            return Response({'status': True,
                             'Response': subject_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class GetSubjectView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    __doc__ = "GET API for subject"

    @swagger_auto_schema(tags=["Subjects"])
    def get(self, request, subject_id=None):
        try:
            subject = self.queryset.get(pk=int(subject_id))
            subject_serializer = self.serializer_class(subject, many=False)
            return Response({'status': True,
                             'Response': subject_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class AddSubjectView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubjectSerializer

    __doc__ = "Create API for subject"

    @swagger_auto_schema(
        operation_description="Create API for subject",
        request_body=SubjectSerializer,
        tags=["Subjects"]
    )
    def post(self, request):
        try:
            subject_serializer = self.serializer_class(data=request.data)
            if subject_serializer.is_valid():
                school = subject_serializer.validated_data["school"]
                if not school.manager == request.user:
                    return Response({'status': False, 'message': "Permission to perform action denied"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                subject_serializer.save()
                return Response({'status': True, 'message': subject_serializer.data}, status.HTTP_201_CREATED)
            else:
                message = ''
                for error in subject_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class UpdateSubjectView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Subject.objects.all()
    serializer_class = SubjectUpdateSerializer

    __doc__ = "Profile Update API for subject"

    @swagger_auto_schema(request_body=SubjectSerializer,tags=["Subjects"],)
    def put(self, request, subject_id=None):
        try:
            subject = self.queryset.get(pk=int(subject_id))
            if not subject.school.manager == request.user:
                return Response({'status': False, 'message': "Permission to perform action denied"},
                                status=status.HTTP_401_UNAUTHORIZED)
            subject_serializer = self.serializer_class(subject, data=request.data)
            if subject_serializer.is_valid():
                subject_serializer.save()
                return Response({'status': True, 'message': subject_serializer.data}, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in subject_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

#############################################
## Teachers
#############################################

class ListTeacherStudentsView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "List a Teacher's sudents in a specific school."

    @swagger_auto_schema(tags=["Teachers"])
    def get(self, request, school_id, teacher_reg_id):
        try:
            teacher_reg_obj = TeacherRegistration.objects.get(pk=int(teacher_reg_id))
            if not (teacher_reg_obj and teacher_reg_obj.is_active):
                return Response({'status': True, 'Response': []}, status=status.HTTP_200_OK)
            teacher_subjects = Subject.objects.filter(school=school_id, teacher=teacher_reg_obj.teacher)

            taught_levels = set()
            for subject in teacher_subjects:
                taught_levels.add(subject.level)
            taught_students = set()

            school_students = StudentRegistration.objects.filter(school=school_id)
            for level in taught_levels:
                taught_students.update(school_students.filter(level=level, is_active=True))

            student_serializer = StudentsSerializer(taught_students, many=True)
            return Response({'status': True,
                             'Response': student_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class ListTeacherSubjectsView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "List a Teacher's subjects in a specific school."

    @swagger_auto_schema(tags=["Teachers"])
    def get(self, request, school_id, teacher_reg_id):
        try:
            teacher_reg_obj = TeacherRegistration.objects.get(pk=int(teacher_reg_id))
            if not (teacher_reg_obj and teacher_reg_obj.is_active):
                return Response({'status': True, 'Response': []}, status=status.HTTP_200_OK)
            teacher_subjects = Subject.objects.filter(school=school_id, teacher=teacher_reg_obj.teacher)
            subject_serializer = SubjectSerializer(teacher_subjects, many=True)
            return Response({'status': True,
                             'Response': subject_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class ListTeachersView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "List Teachers in a specific school."

    @swagger_auto_schema(tags=["Teachers"])
    def get(self, request, school_id):
        try:
            school_teachers = TeacherRegistration.objects.filter(school=school_id, is_active=True)
            teacher_serializer = TeachersSerializer(school_teachers, many=True)
            return Response({'status': True,
                             'Response': teacher_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ListTeachersRegistrationsView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "List Teachers' Registrations."

    @swagger_auto_schema(tags=["Teachers"])
    def get(self, request, teacher_id):
        try:
            teacher = User.objects.get(pk=teacher_id, is_active=True)
            teachers_regs = TeacherRegistration.objects.filter(teacher=teacher, is_active=True)
            teacher_serializer = TeachersSerializer(teachers_regs, many=True)
            return Response({'status': True,
                             'Response': teacher_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateTeacherView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Update Teacher's Registration Information."

    @swagger_auto_schema(request_body=TeachersUpdateSerializer, tags=["Teachers"])
    def put(self, request, teacher_reg_id):
        try:
            school_teacher = TeacherRegistration.objects.get(pk=teacher_reg_id)
            if not ((school_teacher.school.manager == request.user) or (school_teacher.teacher == request.user)):
                return Response({'status': False, 'message': "Permission to perform action denied"},
                                status=status.HTTP_401_UNAUTHORIZED)
            teacher_serializer = TeachersUpdateSerializer(school_teacher, data=request.data, many=False)
            if teacher_serializer.is_valid():
                teacher_serializer.save()
            else:
                raise Exception("Provided data is invalid")
            return Response({'status': True, 'Response': teacher_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AddTeacherView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Register Teacher API"

    @swagger_auto_schema(request_body=TeachersSerializer, tags=["Teachers"])
    def post(self, request):
        try:
            teacher_serializer = TeachersSerializer(data=request.data)
            if teacher_serializer.is_valid():
                data = teacher_serializer.validated_data
                if not data['teacher'].role.lower() == "teacher":
                    raise Exception("User being registered is not a 'teacher'")
                if not data['school'].manager == request.user:
                    return Response({'status': False, 'message': "Permission to perform action denied"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                teacher_serializer.save()
                return Response({'status': True, 'message': teacher_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                message = ''
                for error in teacher_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False, 'message': message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#############################################
## Students
#############################################
class ListStudentsView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "List Students in a specific school."

    @swagger_auto_schema(tags=["Students"])
    def get(self, request, school_id):
        try:
            students = StudentRegistration.objects.filter(school=school_id, is_active=True)
            data = json.loads(serializers.serialize('json', students, use_natural_foreign_keys=True, cls=JsonEncoder))
            return Response({'status': True, 'Response': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ListStudentsRegistrationsView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "List Students' Registrations."

    @swagger_auto_schema(tags=["Students"])
    def get(self, request, student_id):
        try:
            student = User.objects.get(pk=student_id, is_active=True)
            students_regs = StudentRegistration.objects.filter(student=student, is_active=True)
            students_serializer = StudentsSerializer(students_regs, many=True)
            return Response({'status': True,
                             'Response': students_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ListStudentSubjectsView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "List a Student's subjects in a specific school."

    @swagger_auto_schema(tags=["Students"])
    def get(self, request, reg_id):
        try:
            student_reg_obj = StudentRegistration.objects.get(pk=int(reg_id))
            if not (student_reg_obj and student_reg_obj.is_active):
                return Response({'status': True, 'Response': []}, status=status.HTTP_200_OK)
            subject_serializer = SubjectSerializer(student_reg_obj.subjects, many=True)
            return Response({'status': True,
                             'Response': subject_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class AddStudentView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Register Student API"

    @swagger_auto_schema(request_body=StudentsSerializer, tags=["Students"])
    def post(self, request):
        try:
            student_serializer = StudentsSerializer(data=request.data)
            if student_serializer.is_valid():
                data = student_serializer.validated_data
                teacher_regs = TeacherRegistration.objects.filter(school=data['school'])
                teachers = [data['school'].manager, ]
                for reg in teacher_regs:
                    if reg.is_active:
                        teachers.append(reg.teacher)
                if not request.user in teachers:
                    return Response({'status': False, 'message': "Permission to perform action denied"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                student_serializer.save()
                return Response({'status': True, 'message': student_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                message = ''
                for error in student_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False, 'message': message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateStudentView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Update Student's Registration Information."

    @swagger_auto_schema(request_body=StudentsUpdateSerializer, tags=["Students"])
    def put(self, request, member_id):
        try:
            student = StudentRegistration.objects.get(pk=member_id)
            student_serializer = StudentsUpdateSerializer(student, data=request.data)
            if student_serializer.is_valid():
                data = student_serializer.validated_data
                teacher_regs = TeacherRegistration.objects.filter(school=data['school'])
                teachers = [data['school'].manager, ]
                for reg in teacher_regs:
                    if reg.is_active:
                        teachers.append(reg.teacher)
                if not request.user in teachers:
                    return Response({'status': False, 'message': "Permission to perform action denied"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                student_serializer.save()
            else:
                raise Exception("Provided data is invalid")
            return Response({'status': True, 'Response': student_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
