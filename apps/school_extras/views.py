from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
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
from .models import Subject, TeacherRegistration, StudentRegistration, Level
from .serializers import (
        SubjectSerializer,
        SubjectUpdateSerializer,
        TeachersSerializer,
        TeachersUpdateSerializer,
        StudentsSerializer,
        StudentsUpdateSerializer,
        LevelUpdateSerializer,
        LevelSerializer
)


#############################################
## Levels
#############################################
class ListLevelsView(APIView):
    serializer_class = LevelSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(tags=["Schools"])
    def get(self, request, school_id):
        __doc__ = "List all Levels."
        try:
            levels = Level.objects.filter(school=school_id)
            data = json.loads(serializers.serialize('json', levels, use_natural_foreign_keys=True, cls=JsonEncoder))
            return Response({'status': True, 'Response': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetLevelView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

    __doc__ = "GET API for level"

    @swagger_auto_schema(tags=["Schools"])
    def get(self, request, level_id=None):
        try:
            level = self.queryset.get(pk=int(level_id))
            data = json.loads(serializers.serialize('json', [level,], use_natural_foreign_keys=True, cls=JsonEncoder))[0]
            return Response({'status': True, 'Response': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AddLevelView(APIView):
    permission_classes = (IsAuthenticated,)

    __doc__ = "Create API for level"

    @swagger_auto_schema(
        operation_description="Create API for level",
        request_body=LevelSerializer,
        tags=["Schools"]
    )
    def post(self, request):
        try:
            level_serializer = LevelSerializer(data=request.data)
            if level_serializer.is_valid():
                level = teacher_serializer.validated_data
                if not level.school.manager == request.user:
                    return Response({'status': False, 'message': "Permission to add levels is reserved for the school's manager!"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                level_serializer.save()
                data = json.loads(serializers.serialize('json', [level_serializer,], use_natural_foreign_keys=True, cls=JsonEncoder))[0]
                return Response({'status': True, 'message': data}, status.HTTP_201_CREATED)
            else:
                return Response({'status': False, 'message': ','.join(level_serializer.errors.values())}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateLevelView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Level.objects.all()
    serializer_class = LevelUpdateSerializer

    __doc__ = "Profile Update API for level"

    @swagger_auto_schema(request_body=SubjectSerializer,tags=["Schools"],)
    def put(self, request, level_id=None):
        try:
            level = self.queryset.get(pk=int(level_id))
            if not level.school.manager == request.user:
                return Response({'status': False, 'message': "Permission to perform action denied"},
                                status=status.HTTP_401_UNAUTHORIZED)
            level_serializer = self.serializer_class(level, data=request.data)
            if level_serializer.is_valid():
                level_serializer.save()
                data = json.loads(serializers.serialize('json', [level_serializer,], use_natural_foreign_keys=True, cls=JsonEncoder))[0]
                return Response({'status': True, 'message': data}, status=status.HTTP_200_OK)
            else:
                return Response({'status': False, 'message': ','.join(level_serializer.errors.values())}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
            subjects = Subject.objects.filter(level__school=school_id)
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

    __doc__ = "Create API for subject"

    @swagger_auto_schema(
        operation_description="Create API for subject",
        request_body=SubjectSerializer,
        tags=["Subjects"]
    )
    def post(self, request):
        try:
            if not request.data.get("name"):
                raise Exception('"Name" field required.')
            level = get_object_or_404(Level, pk=int(request.data.get("level")))
            if not level.school.manager == request.user:
                return Response({'status': False, 'message': "Permission to add subjects is reserved for the school's manager!"},
                                status=status.HTTP_401_UNAUTHORIZED)
            level.subject_set.create(name=request.data.get("name"), description=request.data.get("description"))
            subjects = SubjectSerializer(Subject.objects.all(), many=True)
            return Response({'status': True, 'message': subjects.data}, status.HTTP_201_CREATED)
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
            teacher_reg_obj = TeacherRegistration.objects.get(pk=int(teacher_reg_id), school=int(school_id))
            taught_levels = set()
            taught_students = set()
            for subject in teacher_reg_obj.subjects.all():
                taught_levels.add(subject.level)

            school_students = StudentRegistration.objects.filter(school=school_id)
            for level in taught_levels:
                taught_students.update(school_students.filter(level=level))

            data = json.loads(serializers.serialize('json', taught_students, use_natural_foreign_keys=True, cls=JsonEncoder))
            return Response({'status': True, 'Response': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class ListTeacherSubjectsView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "List a Teacher's subjects in a specific school."

    @swagger_auto_schema(tags=["Teachers"])
    def get(self, request, school_id, teacher_reg_id):
        try:
            teacher_reg_obj = TeacherRegistration.objects.get(pk=int(teacher_reg_id), school=int(school_id))
            data = json.loads(serializers.serialize('json', teacher_reg_obj.subjects.all(),
                                                    use_natural_foreign_keys=True, cls=JsonEncoder))
            return Response({'status': True, 'Response': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class ListTeachersView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "List Teachers in a specific school."

    @swagger_auto_schema(tags=["Teachers"])
    def get(self, request, school_id):
        try:
            school_teachers = TeacherRegistration.objects.filter(school=school_id)
            data = json.loads(serializers.serialize('json', school_teachers, use_natural_foreign_keys=True, cls=JsonEncoder))
            return Response({'status': True, 'Response': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ListTeachersRegistrationsView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "List Teachers' Registrations."

    @swagger_auto_schema(tags=["Teachers"])
    def get(self, request, teacher_id):
        try:
            teachers_regs = TeacherRegistration.objects.filter(teacher=teacher_id)
            data = json.loads(serializers.serialize('json', teachers_regs, use_natural_foreign_keys=True, cls=JsonEncoder))
            return Response({'status': True, 'Response': data}, status=status.HTTP_200_OK)
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
            students_regs = StudentRegistration.objects.filter(student=student_id)
            data = json.loads(serializers.serialize('json', students_regs, use_natural_foreign_keys=True, cls=JsonEncoder))
            return Response({'status': True, 'Response': data}, status=status.HTTP_200_OK)
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
    def put(self, request, reg_id):
        try:
            student = StudentRegistration.objects.get(pk=reg_id)
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
