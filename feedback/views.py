from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

# local imports
from .models import Feedback
from resources.models import Resource
from core.email_service import send_email
from .serializers import FeedbackSerializer, FeedbackUpdateSerializer


class ListFeedbackView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "List all feedback."

    @swagger_auto_schema(tags=["Feedback"])
    def get(self, request):
        try:
            feedback = Feedback.objects.all()
            feedback_serializer = FeedbackSerializer(feedback, many=True)
            return Response({'status': True,
                             'Response': feedback_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class ListResourceFeedbackView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "List all feedback."

    @swagger_auto_schema(tags=["Feedback"])
    def get(self, request, resource_id):
        try:
            resource = Resource.objects.get(pk=resource_id)
            feedback = Feedback.objects.filter(resource=resource)
            feedback_serializer = FeedbackSerializer(feedback, many=True)
            return Response({'status': True,
                             'Response': feedback_serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class GetFeedbackView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "GET API for feedback"

    @swagger_auto_schema(tags=["Feedback"])
    def get(self, request, feedback_id=None):
        try:
            feedback = Feedback.objects.get(pk=int(feedback_id))
            feedback_serializer = FeedbackSerializer(feedback, many=False)
            return Response({'status': True,
                             'Response': feedback_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class CreateFeedbackView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Create API for feedback"

    @swagger_auto_schema(request_body=FeedbackSerializer, tags=["Feedback"])
    def post(self, request):
        try:
            feedback_serializer = FeedbackSerializer(data=request.data)
            if feedback_serializer.is_valid():
                feedback_serializer.save()
                data = feedback_serializer.validated_data
                send_email(
                    RESOURCE_NAME=data['resource'].name,
                    FEEDBACK_CATEGORY=data['category'],
                    request=request, template="FEEDBACK_CREATED",
                    recipient_list=[data['resource'].created_by.email,]
                )
                return Response({'status': True, 'message': feedback_serializer.data}, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in feedback_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class UpdateFeedbackView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Profile Update API for feedback"

    @swagger_auto_schema(request_body=FeedbackUpdateSerializer, tags=["Feedback"])
    def put(self, request, feedback_id=None):
        try:
            feedback = Feedback.objects.get(pk=int(feedback_id))
            if not feedback.created_by == request.user:
                return Response({'status': False, 'message': "Permission to perform action denied"},
                                status=status.HTTP_401_UNAUTHORIZED)
            feedback_serializer = FeedbackUpdateSerializer(feedback, data=request.data)
            if feedback_serializer.is_valid():
                feedback_serializer.save()
                return Response({'status': True, 'message': feedback_serializer.data}, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in feedback_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
