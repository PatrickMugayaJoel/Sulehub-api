from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core import serializers
import json

# local imports
from .models import School
from .serializers import SchoolSerializer, SchoolUpdateSerializer
from core.upload_service import upload


class ListSchoolsView(APIView):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(tags=["Schools"])
    def get(self, request):
        """
        List all schools.
        """
        try:
            schools = self.queryset.all()
            data = json.loads(serializers.serialize('json', schools, use_natural_foreign_keys=True))
            # school_serializer = self.serializer_class(schools, many=True)
            return Response({'status': True,
                             'Response': data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class GetSchoolView(APIView):
    permission_classes = (AllowAny,)
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    __doc__ = "GET API for school"

    @swagger_auto_schema(tags=["Schools"])
    def get(self, request, school_id=None):
        try:
            school = self.queryset.get(pk=int(school_id))
            data = json.loads(serializers.serialize('json', [school,], use_natural_foreign_keys=True))[0]
            return Response({
                'status': True,
                'Response': data},
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class AddSchoolView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SchoolSerializer

    __doc__ = "Create API for school"

    @swagger_auto_schema(
        operation_description="Create API for school",
        request_body=SchoolSerializer,
        tags=["Schools"]
    )
    def post(self, request):
        try:
            school_serializer = self.serializer_class(data=request.data)
            if school_serializer.is_valid():
                school_serializer.save()
                return Response({'status': True, 'message': school_serializer.data}, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in school_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class UpdateSchoolView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = School.objects.all()
    serializer_class = SchoolUpdateSerializer

    __doc__ = "Profile Update API for school"

    @swagger_auto_schema(request_body=SchoolSerializer,tags=["Schools"])
    def put(self, request, school_id=None):
        try:
            school = self.queryset.get(pk=int(school_id))
            school_serializer = self.serializer_class(school, data=request.data)
            if school_serializer.is_valid():
                if not school.manager == request.user:
                    return Response({'status': False, 'message': "Permission to perform action denied"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                school_serializer.save()
                return Response({'status': True, 'message': school_serializer.data}, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in school_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class SchoolsDPView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = School.objects.all()

    __doc__ = "Update school display picture"

    @swagger_auto_schema(tags=["Schools"],)
    def post(self, request, school_id=None):
        try:
            school = self.queryset.get(pk=int(school_id))
            if not school.manager == request.user:
                return Response({'status': False, 'message': "Permission to perform action denied"},
                                status=status.HTTP_401_UNAUTHORIZED)
            if not request.FILES.get('file'):
                raise ObjectDoesNotExist("'Request File' object is empty")
            filepath = "uploads/pictures/profiles/" + str(request.FILES['file'])
            result = upload(request, filepath, "image")
            if result["status"]:
                school.DP=filepath
                school.save()
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
