from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny

# local imports
from .models import Subject
from .serializers import SubjectSerializer, SubjectUpdateSerializer
from core.email_service import send_email
from core.upload_service import upload


class ListSubjectsView(APIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        List all subjects.
        """
        try:
            subjects = self.queryset.all()
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
        #  responses={200: 'slug not found'}
    )
    def post(self, request):
        try:
            subject_serializer = self.serializer_class(data=request.data)
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

class UpdateSubjectView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Subject.objects.all()
    serializer_class = SubjectUpdateSerializer

    __doc__ = "Profile Update API for subject"

    @swagger_auto_schema(request_body=SubjectSerializer,)
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
