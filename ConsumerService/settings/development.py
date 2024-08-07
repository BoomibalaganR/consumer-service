"""
Developement specific setting
"""
from datetime import timedelta
import mongoengine
import os

from .base import *
DEBUG = os.getenv("DEBUG", "true") == "true"

# MongoDB Atlas connection
# connect(
#     db=os.getenv("MONGO_DB_NAME"),
#     username=os.getenv("MONGO_DB_USER"),
#     password=os.getenv("MONGO_DB_PASSWORD"),
#     host=f"mongodb+srv://{os.getenv('MONGO_DB_USER')}:{os.getenv('MONGO_DB_PASSWORD')}@{
#         os.getenv('MONGO_DB_CLUSTER')}/?retryWrites=true&w=majority",
# )

try:
    mongoengine.connect(
        db='vitagist-DB',
        host='mongodb+srv://boomibalaganR:Boomi1234@cluster0.ue0af0l.mongodb.net/vitagist-DB?retryWrites=true&w=majority&appName=Cluster0',
        username='boomibalaganR',
        password='Boomi1234',
        authentication_source='admin'
    )
    print("cloud DB successfully connected.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}") 

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': ':memory:',
#     }
# }
    # settings.py
REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'common.tokenAuthenticate.CustomJWTAuthentication',
    # ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.getenv("SECRET_KEY", "default-secret-key"),
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'coffer_id',
    'USER_ID_CLAIM': 'coffer_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
}
