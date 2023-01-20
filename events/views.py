from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny

# local imports
from .models import Event
from schools.models import School
from .serializers import EventSerializer, EventUpdateSerializer


class ListEventsView(APIView):
    permission_classes = (AllowAny,)
    __doc__ = "List all events."

    @swagger_auto_schema(tags=["Events"])
    def get(self, request):
        try:
            events = Event.objects.all()
            event_serializer = EventSerializer(events, many=True)
            return Response({'status': True,
                             'Response': event_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class ListSchoolEventsView(APIView):
    permission_classes = (AllowAny,)
    __doc__ = "List all events."

    @swagger_auto_schema(tags=["Events"])
    def get(self, request, school_id):
        try:
            school = School.objects.get(pk=school_id)
            events = Event.objects.filter(school=school)
            event_serializer = EventSerializer(events, many=True)
            return Response({'status': True,
                             'Response': event_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class GetEventView(APIView):
    permission_classes = (AllowAny,)
    __doc__ = "GET API for event"

    @swagger_auto_schema(tags=["Events"])
    def get(self, request, event_id=None):
        try:
            event = Event.objects.get(pk=int(event_id))
            event_serializer = EventSerializer(event, many=False)
            return Response({'status': True,
                             'Response': event_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class CreateEventView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Create API for event"

    @swagger_auto_schema(request_body=EventSerializer, tags=["Events"])
    def post(self, request):
        try:
            event_serializer = EventSerializer(data=request.data)
            if event_serializer.is_valid():
                event_serializer.save()
                return Response({'status': True, 'message': event_serializer.data}, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in event_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class UpdateEventView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Profile Update API for event"

    @swagger_auto_schema(request_body=EventUpdateSerializer, tags=["Events"])
    def put(self, request, event_id=None):
        try:
            event = Event.objects.get(pk=int(event_id))
            event_serializer = EventUpdateSerializer(event, data=request.data)
            if event_serializer.is_valid():
                event_serializer.save()
                return Response({'status': True, 'message': event_serializer.data}, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in event_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
