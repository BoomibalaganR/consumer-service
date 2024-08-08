import jwt
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1] if auth_header else None

        if not token:
            raise NotAuthenticated("Unauthorized")

        try:
            # Decode the JWT token using `simplejwt`
            validated_token = self.get_validated_token(token)
            payload = validated_token.payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Token is invalid")
        except TokenError:
            raise AuthenticationFailed("Token is invalid or expired")

        # try:
        #     user = Consumer.objects.get(coffer_id=payload['coffer_id']) # type: ignore
        # except Consumer.DoesNotExist: # type: ignore
        #     raise AuthenticationFailed('Consumer not found')

        print("Successfully authenticated...")
        return (payload, None)

    def authenticate_header(self, request):
        return "Bearer"
