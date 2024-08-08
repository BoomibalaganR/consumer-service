from api.consumer_profile.models import Consumer
from common.decorator import validatePayload
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import EmailVerificationSerializer, ResendEmailVerificationSerializer
from .services import EmailVerificationService


class EmailVerificationView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    @validatePayload
    def post(self, request, *args, **kwargs):
        email = self.payload["email"]  # type: ignore
        token = self.payload["token"]  # type: ignore

        result = EmailVerificationService.verify_email_token(email, token)
        return Response(result, status=status.HTTP_200_OK)


class ResendEmailVerificationView(generics.GenericAPIView):
    serializer_class = ResendEmailVerificationSerializer

    @validatePayload
    def post(self, request, *args, **kwargs):
        email = self.payload["email"]  # type: ignore
        consumer = Consumer.get_by_email(email)

        resend_token = EmailVerificationService.resend_email_verification(
            consumer.coffer_id
        )
        return Response(
            {
                "message": "Verification email resent successfully.",
                "resend_email_token": resend_token,
            },
            status=status.HTTP_200_OK,
        )
