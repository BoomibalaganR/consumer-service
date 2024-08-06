from .serializers import LoginSerializer
from .models import Consumer
from rest_framework import generics, status

from api.verification.services import EmailVerificationService
from .serializers import ConsumerCreateSerializer, ConsumerDetailSerializer 
from .util import generate_jwt_token
from rest_framework.response import Response
from rest_framework.response import Response 
from rest_framework import status 
from common.decorator import validatePayload


class ConsumerRegisterView(generics.GenericAPIView):
    serializer_class = ConsumerCreateSerializer

    @validatePayload
    def post(self, request, *args, **kwargs):
        
        consumer = self.get_serializer().create(self.payload) # type: ignore

        # Create email verification after registration
        verification_token = EmailVerificationService.create_email_verification(
            consumer.coffer_id)
        return Response({
                        'message': 'Consumer registered successfully. Verification email sent.',
                        'verification_token': verification_token
                        },
                        status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @validatePayload
    def post(self, request, *args, **kwargs):
        email = self.payload['email'] # type: ignore
        password = self.payload['password'] # type: ignore

        consumer = Consumer.get_by_email(email=email)
   
        if not consumer.is_password_match(password):
            return Response(
                {"detail": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if consumer.lastlogin is None: 
            print("==========>>>> WELCOME EMAIL <<<<==============")
      
        serializer = ConsumerDetailSerializer(consumer)
    
        token = generate_jwt_token(consumer)
        consumer.update_lastlogin()

        return Response(
            data={'token': token, 'data': serializer.data},
            status=status.HTTP_200_OK
        )
