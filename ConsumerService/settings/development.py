"""
Developement specific setting
"""

import os
from datetime import timedelta

import mongoengine

from .base import *  # noqa: F403

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
    mongoengine.connect(host=os.getenv("MONGO_DB_URI"))
    print("cloud Consumer DB successfully connected.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

    # settings.py
REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'common.tokenAuthenticate.CustomJWTAuthentication',
    # ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": os.getenv("SECRET_KEY", "default-secret-key"),
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "coffer_id",
    "USER_ID_CLAIM": "coffer_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}
