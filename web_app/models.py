from mongoengine import Document, StringField, DateTimeField, IntField
import datetime
import uuid


class AuthToken(Document):
    __meta__ = {'collection': 'auth_tokens'}
    api_key = StringField(default=str(uuid.uuid4()))
    expiration_date = DateTimeField()
    creation_date = DateTimeField(default=datetime.datetime.now())
    uses = IntField(default=1)


class User(Document):
    __meta__ = {'collection': 'users'}
    username = StringField()
    full_name = StringField()
    uid_number = IntField()
    email = StringField()
