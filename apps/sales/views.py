from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
from apps.utils import JsonEncoder
from django.core import serializers

# local imports
from .models import Sale
from apps.resources.models import Resource
from .serializers import SaleSerializer, SaleUpdateSerializer


class ListSalesView(APIView):
    permission_classes = (AllowAny,)
    __doc__ = "List all sales."

    @swagger_auto_schema(tags=["Sales"])
    def get(self, request):
        try:
            sales = Sale.objects.all()
            data = json.loads(serializers.serialize('json', sales, use_natural_foreign_keys=True, cls=JsonEncoder))
            return Response({'status': True, 'Response': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ListResourceSalesView(APIView):
    permission_classes = (AllowAny,)
    __doc__ = "List all resource sales."

    @swagger_auto_schema(tags=["Sales"])
    def get(self, request, resource_id):
        try:
            sales = Sale.objects.filter(resource=resource_id)
            data = json.loads(serializers.serialize('json', sales, use_natural_foreign_keys=True, cls=JsonEncoder))
            return Response({'status': True, 'Response': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetSaleView(APIView):
    permission_classes = (AllowAny,)
    __doc__ = "GET API for sale"

    @swagger_auto_schema(tags=["Sales"])
    def get(self, request, sale_id=None):
        try:
            sale = Sale.objects.get(pk=int(sale_id))
            data = json.loads(serializers.serialize('json', [sale,], use_natural_foreign_keys=True, cls=JsonEncoder))[0]
            return Response({'status': True, 'Response': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class CreateSaleView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Create API for sale"

    @swagger_auto_schema(request_body=SaleSerializer, tags=["Sales"])
    def post(self, request):
        try:
            sale_serializer = SaleSerializer(data=request.data)
            if sale_serializer.is_valid():
                sale_serializer.save()
                return Response({'status': True, 'message': sale_serializer.data}, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in sale_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

class UpdateSalesView(APIView):
    permission_classes = (IsAuthenticated,)
    __doc__ = "Profile Update API for sale"

    @swagger_auto_schema(request_body=SaleUpdateSerializer, tags=["Sales"])
    def put(self, request, sale_id=None):
        try:
            sale = Sale.objects.get(pk=int(sale_id))
            if not sale.created_by == request.user:
                return Response({'status': False, 'message': "Permission to perform action denied"},
                                status=status.HTTP_401_UNAUTHORIZED)
            sale_serializer = SaleUpdateSerializer(sale, data=request.data)
            if sale_serializer.is_valid():
                sale_serializer.save()
                return Response({'status': True, 'message': sale_serializer.data}, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in sale_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
