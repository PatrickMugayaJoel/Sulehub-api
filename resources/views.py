from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny

# local imports
from .models import Resource
from core.upload_service import upload
from .serializers import ResourceSerializer, ResourceUpdateSerializer


class ListResourcesView(APIView):
    permission_classes = (AllowAny,)
    __doc__ = "List all resources."

    @swagger_auto_schema(tags=["Resources"])
    def get(self, request):
        try:
            resources = Resource.objects.all()
            resource_serializer = ResourceSerializer(resources, many=True)
            return Response({'status': True,
                             'Response': resource_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class GetResourceView(APIView):
    permission_classes = (AllowAny,)
    __doc__ = "GET API for resource"

    @swagger_auto_schema(tags=["Resources"])
    def get(self, request, resource_id=None):
        try:
            resource = Resource.objects.get(pk=int(resource_id))
            resource_serializer = ResourceSerializer(resource, many=False)
            return Response({'status': True,
                             'Response': resource_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class CreateResourceView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Create API for resource"

    @swagger_auto_schema(request_body=ResourceSerializer, tags=["Resources"])
    def post(self, request):
        try:
            resource_serializer = ResourceSerializer(data=request.data)
            if resource_serializer.is_valid():
                resource_serializer.save()
                return Response({'status': True, 'message': resource_serializer.data}, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in resource_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class UpdateResourceView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Profile Update API for resource"

    @swagger_auto_schema(request_body=ResourceUpdateSerializer, tags=["Resources"])
    def put(self, request, resource_id=None):
        try:
            resource = Resource.objects.get(pk=int(resource_id))
            resource_serializer = ResourceUpdateSerializer(resource, data=request.data)
            if resource_serializer.is_valid():
                resource_serializer.save()
                return Response({'status': True, 'message': resource_serializer.data}, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in resource_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class ResourceImageUploadView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Upload resource image"

    @swagger_auto_schema(tags=["Resources"],)
    def post(self, request, resource_id=None):
        try:
            resource = Resource.objects.get(pk=int(resource_id))
            if not request.FILES.get('file'):
                raise ObjectDoesNotExist("'Request File' object is empty")
            filepath = "uploads/pictures/resources/" + str(request.FILES['file'])
            if upload(request, filepath, "image"):
                resource.image=filepath
                resource.save()
                return Response({'status': True,
                                'message': "image successfully uploaded",
                                'path':filepath},
                                status=status.HTTP_200_OK)
            else:
                raise Exception("Upload Request failed!")
        except (AttributeError, ObjectDoesNotExist) as e:
            return Response({'status': False,
                            'message': str(e),},
                            status=status.HTTP_400_BAD_REQUEST)

class ResourceFileUploadView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Upload resource file"

    @swagger_auto_schema(tags=["Resources"],)
    def post(self, request, resource_id=None):
        try:
            resource = Resource.objects.get(pk=int(resource_id))
            if not request.FILES.get('file'):
                raise ObjectDoesNotExist("'Request File' object is empty")
            filepath = "uploads/files/resources/" + str(request.FILES['file'])
            if upload(request, filepath, "document"):
                resource._file=filepath
                resource.is_active=True
                resource.save()
                return Response({'status': True,
                                'message': "file successfully uploaded",
                                'path':filepath},
                                status=status.HTTP_200_OK)
            else:
                raise Exception("Upload Request failed!")
        except (AttributeError, ObjectDoesNotExist) as e:
            return Response({'status': False,
                            'message': str(e),},
                            status=status.HTTP_400_BAD_REQUEST)
