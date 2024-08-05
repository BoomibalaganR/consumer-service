from api.verification.models import EmailVerification
from .serializers import LoginSerializer
from .models import Consumer
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status

from api.verification.services import EmailVerificationService
from .serializers import ConsumerSerializer 
from .util import generate_jwt_token
from rest_framework.response import Response
from rest_framework.response import Response 
from rest_framework import status
from rest_framework import generics

from api.authentication.serializers import ConsumerSerializer

class ConsumerRegisterView(generics.GenericAPIView):
    serializer_class = ConsumerSerializer

    def post(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)  
      
        serializer.is_valid(raise_exception=True) 

        consumer = serializer.save()

        # Create email verification after registration
        verification_token = EmailVerificationService.create_email_verification(consumer.coffer_id)
        return Response({
                        'message': 'Consumer registered successfully. Verification email sent.',
                        'verification_token': verification_token
                        }, 
                        status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        consumer = Consumer.get_by_email(email)

        if not consumer.is_password_match(password):
            return Response(
                {"detail": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        
        consumer_data = {
            "first_name": consumer.first_name,
            "last_name": consumer.last_name,
            "email_verified": EmailVerification.is_email_verified(email),
            "mobile_verified": False, 
            "lastlogin": consumer.lastlogin,
            "email": consumer.email,
            "mobile": consumer.mobile or '',
            "pk": str(consumer.id),
            "password_mode": "normal",
            "uid": consumer.custom_uid(),
        }
        # Update the last login time
        consumer.update_lastlogin()

        # Generate JWT tokens using the utility function
        token = generate_jwt_token(consumer) 
       
        return Response(
            data={'token': token, 'data': consumer_data},
            status=status.HTTP_200_OK
        )
