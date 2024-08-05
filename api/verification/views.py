from rest_framework import generics, status
from rest_framework.response import Response

from api.authentication.models import Consumer
from .serializers import EmailVerificationSerializer, ResendEmailVerificationSerializer
from .services import EmailVerificationService


class EmailVerificationView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        token = serializer.validated_data['token']
        result = EmailVerificationService.verify_email_token(email, token)
        return Response(result, status=status.HTTP_200_OK)


class ResendEmailVerificationView(generics.GenericAPIView):
    serializer_class = ResendEmailVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        consumer = Consumer.get_by_email(email)

        EmailVerificationService.resend_email_verification(consumer.coffer_id)
        return Response({'message': 'Verification email resent successfully.'}, status=status.HTTP_200_OK)
