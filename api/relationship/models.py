from datetime import datetime

from mongoengine import Document, fields


class SpecialRelationship(Document):
    # Choices for the status field
    STATUS_CHOICES = (
        ("requested", "Requested"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    requestor_uid = fields.StringField(required=True)  # Unique ID of the requestor
    requestor_type = fields.StringField(default="consumer")
    requestor_group_acls = fields.ListField(fields.StringField(), default=list)
    requestor_tags = fields.ListField(
        fields.StringField(), default=["personal"]
    )  # Tags for requestor

    acceptor_uid = fields.StringField(required=True)  # Unique ID of the acceptor
    acceptor_type = fields.StringField(default="consumer")
    acceptor_tags = fields.ListField(
        fields.StringField(), default=["personal"]
    )  # Tags for acceptor
    accepted_date = fields.DateTimeField()  # Date when the request was accepted
    acceptor_group_acls = fields.ListField(fields.StringField(), default=list)
    isaccepted = fields.BooleanField(default=False)  # Whether the request is accepted
    status = fields.StringField(choices=STATUS_CHOICES, default="requested")
    description = fields.StringField()  # Description of the relationship
    reject_reason = fields.StringField()  # Reason for rejection
    created = fields.DateTimeField(default=datetime.utcnow)
    tcfilename = fields.StringField()  # Filename for terms and conditions

    @classmethod
    def is_exit(cls, requestor_coffer_id, acceptor_coffer_id):
        relationship_exists = (
            SpecialRelationship.objects(  # type: ignore
                __raw__={
                    "$or": [
                        {
                            "requestor_uid": requestor_coffer_id,
                            "acceptor_uid": acceptor_coffer_id,
                        },
                        {
                            "requestor_uid": acceptor_coffer_id,
                            "acceptor_uid": requestor_coffer_id,
                        },
                    ]
                }
            ).count()
            > 0
        )
        return relationship_exists
