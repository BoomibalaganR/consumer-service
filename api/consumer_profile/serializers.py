from api.consumer_profile.models import Consumer
from api.verification.models import EmailVerification
from rest_framework import serializers


class ConsumerProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    last_name = serializers.CharField()
    dob = serializers.DateTimeField(allow_null=True, format="%d/%m/%Y")  # type: ignore
    email = serializers.EmailField()
    mobile = serializers.CharField()
    citizen = serializers.SerializerMethodField()
    joined = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ")  # type: ignore
    coffer_id = serializers.CharField()
    email_verified = serializers.SerializerMethodField()
    mobile_verified = serializers.SerializerMethodField()
    keepass_filename = serializers.CharField(allow_null=True, required=False)

    def get_citizen(self, consumer):
        citizen_data = []
        for citizen_record in consumer.citizen:
            citizen_details = {
                "country": citizen_record.country,
                "affiliation_type": citizen_record.affiliation_type,
                "mobile_phone": citizen_record.mobile_phone,
                "home_address": citizen_record.home_address,
                "alt_phone": citizen_record.alt_phone,
                "index": citizen_record.index,
                "work_phone": citizen_record.work_phone,
                "work_address": citizen_record.work_address,
            }
            citizen_data.append(citizen_details)
        return citizen_data

    def get_email_verified(self, obj):
        return EmailVerification.is_email_verified(obj.email)  # type: ignore

    def get_mobile_verified(self, obj):
        return False


class UpdateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    middle_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    dob = serializers.DateTimeField(required=False, format="%d/%m/%Y")  # type: ignore
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(required=False)

    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    def validate(self, data):
        request = self.context["request"]
        coffer_id = request.user.get("coffer_id")

        old_password = data.get("old_password", None)
        new_password = data.get("new_password", None)
        confirm_password = data.get("confirm_password", None)

        if old_password and new_password and confirm_password:
            con_obj = Consumer.get_by_coffer_id(coffer_id)
            if old_password and not con_obj.is_password_match(old_password):
                raise serializers.ValidationError(
                    {"old_password": "Old password is incorrect."}
                )

            if new_password != confirm_password:
                raise serializers.ValidationError(
                    {
                        "confirm_password": "New password and confirm password do not match."
                    }
                )
            if "email" in data:
                data.pop("email")
            # hash the new password and remove old, new, and confirm password fields from the data
            data["password"] = Consumer.hash_password(new_password)
            data.pop("old_password", None)
            data.pop("new_password", None)
            data.pop("confirm_password", None)

        return data
