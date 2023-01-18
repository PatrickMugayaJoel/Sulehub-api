from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny

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
    queryset = Subject.objects.all()
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(tags=["Subjects"])
    def get(self, request, school_id):
        __doc__ = "List all subjects."
        try:
            subjects = self.queryset.filter(school=school_id)
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

class UpdateTeacherView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Update Teacher's Registration Information."

    @swagger_auto_schema(request_body=TeachersUpdateSerializer, tags=["Teachers"])
    def put(self, request, teacher_reg_id):
        try:
            school_teachers = TeacherRegistration.objects.get(pk=teacher_reg_id)
            teacher_serializer = TeachersUpdateSerializer(school_teachers, data=request.data, many=False)
            if teacher_serializer.is_valid():
                teacher_serializer.save()
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
            students_serializer = StudentsSerializer(students, many=True)
            return Response({'status': True, 'Response': students_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ListStudentSubjectsView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "List a Student's subjects in a specific school."

    @swagger_auto_schema(tags=["Students"])
    def get(self, request, school_id, student_reg_id):
        try:
            student_reg_obj = StudentRegistration.objects.get(pk=int(student_reg_id))
            if not (student_reg_obj and student_reg_obj.is_active):
                return Response({'status': True, 'Response': []}, status=status.HTTP_200_OK)
            student_subjects = Subject.objects.filter(school=school_id, level=student_reg_obj.level)
            subject_serializer = SubjectSerializer(student_subjects, many=True)
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
    def put(self, request, student_reg_id):
        try:
            student = StudentRegistration.objects.get(pk=student_reg_id)
            student_serializer = StudentsUpdateSerializer(student, data=request.data)
            if student_serializer.is_valid():
                print("yess")
                student_serializer.save()
            return Response({'status': True, 'Response': student_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
