from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import  AuthenticationFailed, NotAuthenticated
import jwt

from api.authentication.models import Consumer


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        token = auth_header and auth_header.split(' ')[1] 
        
        if not token:
            raise NotAuthenticated("UnAuthorized")

        # try:
        #     prefix, token = auth_header.split(' ')
        #     if prefix.lower() != 'bearer':
        #         raise exceptions.AuthenticationFailed(
        #             'Authorization header must start with Bearer')
        # except ValueError:
        #     raise exceptions.AuthenticationFailed(
        #         'Invalid Authorization header format')

        try:
            # Decode the JWT token using `simplejwt`'
            payload = self.get_validated_token(token).payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        try:
            user = Consumer.objects.get(coffer_id=payload['coffer_id']) # type: ignore
        except Consumer.DoesNotExist: # type: ignore
            raise AuthenticationFailed('consumer not found')

        request.user = payload 
        print('successfully authicated...', request.user)
        

    def authenticate_header(self, request):
        return 'Bearer'
