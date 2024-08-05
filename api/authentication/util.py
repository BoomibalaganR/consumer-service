# jwt_utils.py
from rest_framework_simplejwt.tokens import AccessToken


def generate_jwt_token(consumer):
    
    access_token = AccessToken.for_user(consumer)
    access_token['pk'] = str(consumer.id ) 
    
    return str(access_token)
