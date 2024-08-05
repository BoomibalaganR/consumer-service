from datetime import datetime
from mongoengine import Document, fields 
from rest_framework.exceptions import NotFound



class EmailVerification(Document):
    """
    Model for storing email verification tokens.
    """
    # coffer_id = fields.StringField(required=True, unique=True)
    email = fields.EmailField(required=True, unique=True)
    token = fields.StringField(required=True)
    timestamp = fields.DateTimeField(default=datetime.utcnow, required=True)
    is_verified = fields.BooleanField(default=False)

    meta = {'indexes': ['email']}

   
    # @classmethod
    # def get_by_coffer_id(cls, coffer_id):
    #     verification_record = cls.objects(coffer_id=coffer_id).first()  # type: ignore
    #     if not verification_record:
    #         raise NotFound(
    #             "No email verification record found for the provided coffer ID.")
    #     return verification_record

    @classmethod
    def get_by_email(cls, email): 
        verification_record = cls.objects(email=email).first()  # type: ignore
        if not verification_record:
            raise NotFound(
                "Given email is not verified")
        return verification_record
        
    @classmethod
    def is_email_verified(cls, email):
        verification = cls.objects(email=email).first()  # type: ignore
        return verification.is_verified if verification else False