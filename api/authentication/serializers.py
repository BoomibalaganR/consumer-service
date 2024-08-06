from api.verification.models import EmailVerification
from .models import Consumer
from rest_framework import serializers
from .models import Consumer, Country
from django.contrib.auth.hashers import make_password


class ConsumerCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(max_length=10, required=False)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    country = serializers.CharField(required=True) 

    def validate(self, data):
        print('inside validate function')
        # Check if either email or mobile is provided
        if not data.get('email') and not data.get('mobile'):
            raise serializers.ValidationError(
                {"non_field_errors": [
                    "Either email or mobile must be provided."]}
            )

        # Check if passwords and confirm password
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"confirm_password": ["Passwords do not match with password."]}
            )

        # Check if email is already registered
        if 'email' in data:
            if Consumer.objects(email=data['email'].lower()).first(): # type: ignore
                raise serializers.ValidationError(
                    {"email": ["Email is already registered."]}
                )

        # Check if mobile number is already registered
        if 'mobile' in data:
            if Consumer.objects(mobile=data['mobile']).first(): # type: ignore
                raise serializers.ValidationError(
                    {"mobile": ["Mobile number is already registered."]}
                )

        return data

    def create(self, validated_data): 
        print('inside serailzer create....')
        validated_data.pop('confirm_password')

        validated_data['coffer_id'] = Consumer.generate_coffer_id()
        validated_data['password'] = make_password(validated_data['password'])

        # Create Country instance
        country_data = {
            'index': 'citizen_primary',
            'country': validated_data.get('country', ''),
            'affiliation_type': 'citz',
            'mobile_phone': validated_data.get('mobile', '')
        }
        country = Country(**country_data)
        
        # Create Consumer instance
        consumer = Consumer( **validated_data, citizen=[country] )   
        consumer.save()  
        
        return consumer


class ConsumerDetailSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email_verified = serializers.SerializerMethodField()
    mobile_verified = serializers.SerializerMethodField()
    lastlogin = serializers.DateTimeField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    pk = serializers.CharField(source='id')
    password_mode = serializers.CharField(default="normal")
    uid = serializers.SerializerMethodField()

    def get_email_verified(self, obj):
        return EmailVerification.is_email_verified(obj.email)  # type: ignore

    def get_mobile_verified(self, obj):
        return False

    def get_uid(self, obj):
        return obj.custom_uid()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
