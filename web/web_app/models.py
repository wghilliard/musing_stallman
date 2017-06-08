from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField
import datetime
import uuid


class AuthToken(Document):
    __meta__ = {'collection': 'auth_tokens'}
    api_key = StringField(default=str(uuid.uuid4()))
    expiration_date = DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=1))
    creation_date = DateTimeField(default=datetime.datetime.now())
    uses = IntField(default=1)


class User(Document):
    __meta__ = {'collection': 'users'}
    username = StringField(required=True)
    full_name = StringField(required=True)
    email = StringField(required=True)
    uid_number = IntField(default=None)
    password = StringField(default=None)
    has_ldap_account = BooleanField(default=False)
