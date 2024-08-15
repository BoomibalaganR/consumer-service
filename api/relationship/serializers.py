from api.consumer_profile.models import Consumer
from rest_framework import serializers


class RelationshipRequestSerializer(serializers.Serializer):
    consumerId = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)


class RetrieveRelationshipSerializer(serializers.Serializer):
    id = serializers.CharField()
    isSpecial = serializers.BooleanField(default=True)
    canAccept = serializers.BooleanField(default=False)
    business_name = serializers.CharField(default="")
    business_category = serializers.CharField(default="")
    products = serializers.ListField(child=serializers.CharField(), default=[])
    description = serializers.CharField(default="")
    isaccepted = serializers.BooleanField()
    isarchived = serializers.BooleanField(default=False)
    status = serializers.CharField()
    documents = serializers.DictField(default={})
    profile = serializers.DictField(default={})
    biztype = serializers.CharField(default="consumer")
    email = serializers.EmailField(default="")
    mobile = serializers.CharField(default="")
    guid = serializers.CharField(default="")
    tags = serializers.ListField(child=serializers.CharField(), default=[])
    profileUrl = serializers.CharField(default="")

    def to_representation(self, document):
        # Get the default representation from the parent class
        representation = super().to_representation(document)

        # Get request obj from context data
        request_obj = self.context.get("request")
        coffer_id = request_obj.user.get("coffer_id")  # type: ignore
        consumer = self.get_consumer(document, coffer_id)

        # Customize the representation
        representation.update(
            {
                "business_name": consumer.get_full_name(),  # type: ignore
                "biztype": "consumer" if consumer else "",
                "guid": consumer.custom_uid(),  # type: ignore
                "tags": document["acceptor_tags"]
                if document["acceptor_uid"] == coffer_id
                else document["requestor_tags"],
                "profileUrl": consumer.get_profile_url(),  # type: ignore
            }
        )

        return representation

    def get_consumer(self, document, coffer_id):
        if (
            document["acceptor_uid"] == coffer_id
            and document["requestor_type"] == "consumer"
        ):
            return Consumer.get_by_coffer_id(document["requestor_uid"])
        elif (
            document["requestor_uid"] == coffer_id
            and document["acceptor_type"] == "consumer"
        ):
            return Consumer.get_by_coffer_id(document["acceptor_uid"])
        return None
