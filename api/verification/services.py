from datetime import datetime
import os
from api.authentication.models import Consumer
from .models import EmailVerification
from rest_framework.exceptions import ValidationError


class EmailVerificationService: 

    @staticmethod
    def generate_token():
        return os.urandom(8).hex() 
    
    @staticmethod
    def create_email_verification(coffer_id):
        
        consumer = Consumer.get_by_coffer_id(coffer_id)
        token = EmailVerificationService.generate_token()

        email_verification = EmailVerification(
            email=consumer.email,
            token=token,
            timestamp=datetime.utcnow()
        )
        email_verification.save()

        return EmailVerificationService.send_verification_email(consumer, token)

    @staticmethod
    def verify_email_token(email, token):

        consumer = Consumer.get_by_email(email)
        verification_record = EmailVerification.get_by_email(consumer.email) 
        if verification_record.is_verified:
            raise ValidationError(
                {'detail': 'The email has already been verified.'})

        if verification_record.token != token: 
            raise ValidationError({'detail': 'Invalid token'})
            
        
        verification_record.is_verified = True
        verification_record.save()
        return {'message': 'Email verified successfully.'}

    @staticmethod
    def resend_email_verification(coffer_id):

        consumer = Consumer.get_by_coffer_id(coffer_id)
        verification_record = EmailVerification.get_by_email(consumer.email)

        if verification_record.is_verified:
            raise ValidationError(
                {'detail': 'The email has already been verified.'})

        token = EmailVerificationService.generate_token()
        verification_record.token = token
        verification_record.timestamp = datetime.utcnow()
        verification_record.save()

        return EmailVerificationService.send_verification_email(
            consumer, token, subject="Resend Email Verification")

    @staticmethod
    def send_verification_email(consumer, token, subject="Email Verification"):
        payload = {
            "template": "consumer_email_verify",
            "to": [consumer.email],
            "subject": subject,
            "context": {
                "name": f"{consumer.first_name} {consumer.last_name}",
                "token": token
            }
        }
        print("\n<<<<<<<================================================>>>>>>>>>>")
        print(payload)
        print("<<<<<<<================================================>>>>>>>>>>\n")
        return token # for developement purpose
    
   
    