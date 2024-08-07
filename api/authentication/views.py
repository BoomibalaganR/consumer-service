
from api.verification.models import EmailVerification
from .serializers import LoginSerializer
from api.consumer_profile.models import Consumer, Country
from rest_framework import generics, status

from api.verification.services import EmailVerificationService
from .serializers import ConsumerCreateSerializer, ConsumerAuthResponseSerializer, ForgotPasswordSerializer,VerifyPasswordTokenSerializer, ResendPasswordTokenSerializer
from .util import generate_jwt_token, send_password_reset_email, send_password_change_email
from rest_framework.response import Response
from rest_framework.response import Response 
from rest_framework import status 
from common.decorator import validatePayload 


from django.contrib.auth.hashers import make_password

class ConsumerRegisterView(generics.GenericAPIView):
    serializer_class = ConsumerCreateSerializer

    @validatePayload
    def post(self, request, *args, **kwargs):
    
        self.payload.pop('confirm_password') # type: ignore

        self.payload['coffer_id'] = Consumer.generate_coffer_id() # type: ignore
        self.payload['password'] = make_password(self.payload['password'])  # type: ignore

        # Create Country instance
        country_data = {
            'index': 'citizen_primary',
            'country': self.payload.get('country', ''), # type: ignore
            'affiliation_type': 'citz',
            'mobile_phone': self.payload.get('mobile', '') # type: ignore
        }
        country = Country(**country_data)
        
        # Create Consumer instance
        consumer = Consumer( **self.payload, citizen=[country] )    # type: ignore
        consumer.save()  
        
        # return consumer
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
      
        serializer = ConsumerAuthResponseSerializer(consumer)
    
        token = generate_jwt_token(consumer)
        consumer.update_lastlogin()

        return Response(
            data={'token': token, 'data': serializer.data},
            status=status.HTTP_200_OK
        )


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    @validatePayload
    def post(self, request, *args, **kwargs):
       
        email = self.payload['email'] # type: ignore

        consumer = Consumer.get_by_email(email=email) # type: ignore
       
        # Generate a reset token
        token = consumer.generate_password_reset_token() 
        if EmailVerification.is_email_verified(consumer.email):
            send_password_reset_email(consumer=consumer, token=token)

        return Response({'detail': 'A token to reset your password is sent to your email. It is valid for 5 mins',
                         'reset-token': token},
                        status=status.HTTP_200_OK)


class VerifyPasswordTokenView(generics.GenericAPIView):
    serializer_class = VerifyPasswordTokenSerializer

    @validatePayload
    def post(self, request, *args, **kwargs):
        
        email = self.payload['email'] # type: ignore
        password = self.payload['password'] # type: ignore

        
        consumer = Consumer.get_by_email(email=email)
        consumer.set_password(password)
        if EmailVerification.is_email_verified(consumer.email):
            send_password_change_email(consumer=consumer)

        return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)


class ResendPasswordTokenView(generics.GenericAPIView):
    serializer_class = ResendPasswordTokenSerializer

    @validatePayload
    def post(self, request, *args, **kwargs):
        
        email = self.payload['email'] # type: ignore
        consumer = Consumer.get_by_email(email=email)
        
        # Generate a reset token
        token = consumer.generate_password_reset_token()
        if EmailVerification.is_email_verified(consumer.email): 
            send_password_reset_email(consumer=consumer, token=token)

        return Response({'detail': 'A token to reset your password is sent to your email. It is valid for 5 mins',
                         'reset-token': token}, status=status.HTTP_200_OK)
