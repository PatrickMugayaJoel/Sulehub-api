from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core import serializers
from apps.utils import JsonEncoder
import json

# local imports
from .models import Event, Invitation
from apps.schools.models import School
from core.email_service import send_email
from .serializers import EventSerializer, EventUpdateSerializer, InvitationSerializer


class ListEventsView(APIView):
    permission_classes = (AllowAny,)
    __doc__ = "List all events."

    @swagger_auto_schema(tags=["Events"])
    def get(self, request):
        try:
            events = Event.objects.all()
            data = json.loads(serializers.serialize('json', events, use_natural_foreign_keys=True, cls=JsonEncoder))
            return Response({'status': True, 'Response': data}, status=status.HTTP_200_OK)
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
            data = json.loads(serializers.serialize('json', events, use_natural_foreign_keys=True, cls=JsonEncoder))
            return Response({'status': True, 'Response': data}, status=status.HTTP_200_OK)
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
            data = json.loads(serializers.serialize('json', [event,], use_natural_foreign_keys=True, cls=JsonEncoder))[0]
            return Response({'status': True,
                             'Response': data}, status=status.HTTP_200_OK)
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
                school = event_serializer.validated_data['school']
                if not school.manager == request.user:
                    return Response({'status': False, 'message': "Permission to perform action denied"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                event_serializer.save()
                data = event_serializer.data
                send_email(request=request, template="EVENT_CREATED",
                           EVENT_NAME=data['name'], SCHOOL_NAME=school.name,
                    recipient_list=[school.manager.email,]
                )
                return Response({'status': True, 'message': data}, status=status.HTTP_200_OK)
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
            if not ((event.created_by == request.user) or (event.school.manager == request.user)):
                return Response({'status': False, 'message': "Permission to perform action denied"},
                                status=status.HTTP_401_UNAUTHORIZED)
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

class ListInvitationsView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "List invitations."

    @swagger_auto_schema(tags=["Schools"])
    def get(self, request, school_id=0):
        try:
            invites = Invitation.objects.filter(school__pk=int(school_id))
            data = json.loads(serializers.serialize('json', invites, use_natural_foreign_keys=True, cls=JsonEncoder))
            return Response({'status': True, 'Response': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
