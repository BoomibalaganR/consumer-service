from datetime import datetime
import os
from mongoengine import Document, EmbeddedDocument, fields

from django.contrib.auth.hashers import check_password, make_password
from rest_framework.exceptions import NotFound

# from django.utils.crypto import get_random_string 

class Country(EmbeddedDocument):
    index = fields.StringField()
    country = fields.StringField()
    affiliation_type = fields.StringField()
    work_address = fields.StringField()
    home_address = fields.StringField()
    mobile_phone = fields.StringField()
    work_phone = fields.StringField()
    alt_phone = fields.StringField()
    affiliation_countryid = fields.StringField()


class Consumer(Document):
    coffer_id = fields.StringField(unique=True)

    first_name = fields.StringField()
    middle_name = fields.StringField()
    last_name = fields.StringField()
    country = fields.StringField()
    gender = fields.StringField()
    dob = fields.DateTimeField()  
        
    username = fields.StringField()
    password = fields.StringField()
    confirm_password = fields.StringField()
    password_reset_token = fields.StringField()
    password_reset_timestamp = fields.DateTimeField()
    password_mode = fields.StringField()
    joined = fields.DateTimeField(default=datetime.utcnow)
    lastlogin = fields.DateTimeField()

    email = fields.EmailField()
    mobile = fields.StringField()
    email_hash = fields.StringField()
    mobile_hash = fields.StringField()
    citizen = fields.EmbeddedDocumentListField(Country)

    meta = {'collection': 'consumers',
            'indexes': ['coffer_id']}

    @classmethod
    def generate_coffer_id(cls):
        uid = os.urandom(8).hex().upper()
        if Consumer.objects(coffer_id=uid): # type: ignore
            return cls.generate_coffer_id()  # Recursive call
        return uid

    @classmethod
    def get_by_coffer_id(cls, coffer_id):
        consumer = cls.objects(coffer_id=coffer_id).first()  # type: ignore
        if not consumer:
            raise NotFound(
                "Consumer with the provided coffer ID does not exist.")
        return consumer

    @classmethod
    def get_by_email(cls, email):
        consumer = cls.objects(email=email).first()  # type: ignore
        if not consumer:
            raise NotFound("Consumer with the provided email does not exist.")
        return consumer

    def save(self, *args, **kwargs):
            if not self.joined:
                self.joined = datetime.utcnow()
            return super(Consumer, self).save(*args, **kwargs)

    def is_password_match(self, password):
        return check_password(password, self.password) # type: ignore

    def custom_uid(self):
        if self.email:
            return self.email.replace('.', '').replace('@', '').strip() # type: ignore
        elif self.mobile:
            return self.mobile.strip() # type: ignore
        return None 
    
    def update_lastlogin(self): 
        self.lastlogin = datetime.utcnow()
        self.save() 

    def generate_password_reset_token(self):  
        if self.password_reset_token is None: 
            token = os.urandom(5).hex().lower()
            self.password_reset_token = token
        self.password_reset_timestamp = datetime.utcnow()
        self.save() 
        return self.password_reset_token

    def set_password(self, newPassword): 
        self.password = make_password(newPassword) 
        self.password_reset_token = None  # Clear the reset token
        self.password_reset_timestamp = None  # Clear the timestamp
        self.save()
