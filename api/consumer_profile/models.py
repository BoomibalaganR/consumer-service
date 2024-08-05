from mongoengine import Document, fields
from authentication.models import Consumer
# from verification.models import EmailVerification, MobileVerification


class ConsumerProfile(Document):
    consumer = fields.ReferenceField(Consumer, required=True)
    email_verified = fields.BooleanField(default=False)
    mobile_verified = fields.BooleanField(default=False)
    profile_completeness = fields.IntField()
    otp = fields.DictField()
    keepass_filename = fields.StringField()
    ciphertext = fields.StringField()
    profilepic_filename = fields.StringField()
    profilepic_content_type = fields.StringField()
  
    # def update_verification_status(self):
    #     email_verification = EmailVerification.objects(
    #         consumer=self.consumer).first()
    #     self.email_verified = email_verification.is_verified if email_verification else False

    #     mobile_verification = MobileVerification.objects(
    #         consumer=self.consumer).first()
    #     self.mobile_verified = mobile_verification.is_verified if mobile_verification else False

    #     self.save()
