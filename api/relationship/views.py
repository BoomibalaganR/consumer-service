from datetime import datetime

from api.consumer_profile.models import Consumer
from api.relationship.models import SpecialRelationship
from api.relationship.serializers import (
    RelationshipRequestSerializer,
    RetrieveRelationshipSerializer,
)
from common.tokenAuthenticate import CustomJWTAuthentication
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response


class CreateRelationshipView(generics.CreateAPIView):
    serializer_class = RelationshipRequestSerializer
    authentication_classes = [CustomJWTAuthentication]

    def perform_create(self, serializer):
        requestor_coffer_id = self.request.user.get("coffer_id")  # type: ignore
        acceptor_consumer_id = serializer.validated_data.get("consumerId")
        description = serializer.validated_data.get("description")

        requestor_consumer = Consumer.exists_by_coffer_id(coffer_id=requestor_coffer_id)
        acceptor_consumer = Consumer.objects(id=acceptor_consumer_id).first()  # type: ignore

        if not requestor_consumer:
            raise ValidationError({"detail": "Requestor consumer not found."})

        if not acceptor_consumer:
            raise ValidationError({"detail": "Acceptor consumer not found."})

        acceptor_coffer_id = acceptor_consumer.coffer_id

        if requestor_coffer_id == acceptor_coffer_id:
            raise ValidationError(
                {"detail": "Operation not permitted. You cannot request to yourself."}
            )

        relationship_exists = SpecialRelationship.is_exit(
            requestor_coffer_id, acceptor_coffer_id
        )

        if relationship_exists:
            raise ValidationError({"detail": "Relationship already exists."})

        SpecialRelationship.objects.create(  # type: ignore
            acceptor_uid=acceptor_coffer_id,
            requestor_uid=requestor_coffer_id,
            description=description,
        )

        # sending an email notification
        print(">>>>>> SEND EMAIL NOTIFICATION <<<<<<")
        print("Successfully sent request")

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(
            {"message": "Request sent successfully."}, status=status.HTTP_201_CREATED
        )


class AcceptRelationshipView(generics.UpdateAPIView):
    authentication_classes = [CustomJWTAuthentication]

    def get_object(self):
        rel_id = self.kwargs.get("rel_id")

        try:
            relationship = SpecialRelationship.objects.get(id=rel_id)  # type: ignore
        except SpecialRelationship.DoesNotExist:  # type: ignore
            raise NotFound("Relationship not found.")
        return relationship

    def patch(self, request, *args, **kwargs):
        relationship = self.get_object()
        coffer_id = request.user.get("coffer_id")
        if relationship.requestor_uid == coffer_id:
            raise ValidationError(
                {
                    "detail": "Operation not permitted. You cannot accept your own request."
                }
            )

        # Check if the relationship is already accepted
        if relationship.isaccepted:
            raise ValidationError({"detail": "Relationship is already accepted."})

        # Update the relationship
        relationship.isaccepted = True
        relationship.accepted_date = datetime.utcnow()
        relationship.status = "accepted"
        relationship.save()

        print(">>>>>> SEND EMAIL NOTIFICATION <<<<<<")
        print("Successfully accepted request")

        return Response(
            {"message": "Relationship accepted successfully."},
            status=status.HTTP_200_OK,
        )


class ListRelationshipsView(generics.ListAPIView):
    serializer_class = RetrieveRelationshipSerializer
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        coffer_id = self.request.user.get("coffer_id")  # type: ignore
        return SpecialRelationship.objects(  # type: ignore
            __raw__={"$or": [{"acceptor_uid": coffer_id}, {"requestor_uid": coffer_id}]}
        )

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({"data": response.data}, status=status.HTTP_200_OK)


class GetRelationshipsByIdView(generics.RetrieveAPIView):
    serializer_class = RetrieveRelationshipSerializer
    authentication_classes = [CustomJWTAuthentication]

    def get_object(self):
        rel_id = self.kwargs.get("rel_id")

        try:
            return SpecialRelationship.objects.get(  # type: ignore
                id=rel_id
            )
        except SpecialRelationship.DoesNotExist:  # type: ignore
            raise NotFound({"detail": "Relationship not found."})

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({"data": response.data}, status=status.HTTP_200_OK)
