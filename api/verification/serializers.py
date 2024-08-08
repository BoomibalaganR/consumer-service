from rest_framework import serializers


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Email is required.",
            "blank": "Email cannot be empty.",
            "invalid": "Enter a valid email address.",
        },
    )
    token = serializers.CharField(
        required=True,
        error_messages={
            "required": "Token is required.",
            "blank": "token cannot be empty.",
        },
    )


class ResendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Email is required.",
            "blank": "Email cannot be empty.",
            "invalid": "Enter a valid email address.",
        },
    )
