from rest_framework import serializers 
from api.verification.models import EmailVerification


class ConsumerProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    last_name = serializers.CharField()
    dob = serializers.DateTimeField( allow_null=True, format='%d/%m/%Y')  # type: ignore
    email = serializers.EmailField()
    mobile = serializers.CharField()
    citizen = serializers.SerializerMethodField()
    joined = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ') # type: ignore
    coffer_id = serializers.CharField()
    email_verified = serializers.SerializerMethodField()
    mobile_verified = serializers.SerializerMethodField()
    keepass_filename = serializers.CharField(allow_null=True, required=False)

    def get_citizen(self, consumer):
        citizen_data = []
        for citizen_record in consumer.citizen:
            citizen_details = {
                'country': citizen_record.country,
                'affiliation_type': citizen_record.affiliation_type,
                'mobile_phone': citizen_record.mobile_phone,
                'home_address': citizen_record.home_address,
                'alt_phone': citizen_record.alt_phone,
                'index': citizen_record.index,
                'work_phone': citizen_record.work_phone,
                'work_address': citizen_record.work_address
            }
            citizen_data.append(citizen_details)
        return citizen_data

    def get_email_verified(self, obj):
        return EmailVerification.is_email_verified(obj.email)  # type: ignore

    def get_mobile_verified(self, obj):
        return False
