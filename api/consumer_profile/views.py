# authentication/views.py
from rest_framework import generics, status
from rest_framework.response import Response

from common.tokenAuthenticate import CustomJWTAuthentication
from .models import Consumer
from .serializers import ConsumerProfileSerializer

from rest_framework.permissions import IsAuthenticated


class ConsumerProfileDetailView(generics.GenericAPIView):
    authentication_classes = [CustomJWTAuthentication] 
   
    def get(self, request, *args, **kwargs): 
        
        coffer_id =   request.user.get('coffer_id', None) 
        consumer = Consumer.get_by_coffer_id(coffer_id)
        serializer = ConsumerProfileSerializer(consumer) 
        
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    