from api.authentication.util import send_password_change_email
from common.decorator import validatePayload
from common.tokenAuthenticate import CustomJWTAuthentication
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Consumer
from .serializers import ConsumerProfileSerializer, UpdateProfileSerializer


class ConsumerProfileView(generics.GenericAPIView):
    authentication_classes = [CustomJWTAuthentication]
    serializer_class = UpdateProfileSerializer

    def get(self, request, *args, **kwargs):
        coffer_id = request.user.get("coffer_id", None)
        consumer = Consumer.get_by_coffer_id(coffer_id)
        serializer = ConsumerProfileSerializer(consumer)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @validatePayload
    def put(self, request, *args, **kwargs):
        coffer_id = request.user.get("coffer_id")
        update_fields = self.payload.copy()  # type: ignore

        # Convert to MongoEngine update format like {'set__first_name': 'boomi', 'set__last_name': 'R'}
        update_dict = {f"set__{key}": value for key, value in update_fields.items()}

        # Update document and return the updated document
        updated_consumer = Consumer.objects(coffer_id=coffer_id).modify(  # type: ignore
            new=True, **update_dict
        )

        # Send email if password was updated
        if "password" in update_fields:
            send_password_change_email(updated_consumer)

        return Response(
            {"detail": "Profile updated successfully."},
            status=status.HTTP_200_OK,
        )
