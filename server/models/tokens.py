from datetime import datetime, timedelta
from mongoengine import (
    connect,
    DateTimeField,
    Document,
    IntField,
    StringField,
    ObjectIdField
)
from pymongo import MongoClient
import json

import settings

connect(settings.DB)
client = MongoClient('localhost', 27017)

class Tokens(Document):
    def __init__(self, kwargs):
        super(Tokens, self).__init__(**kwargs)
        try:
            self.access_token = kwargs['access_token']
            self.refresh_token = kwargs['refresh_token']
            self.scope = kwargs['scope']
            self.token_type = kwargs['token_type']

            self.curr_time = datetime.now()
            self.expires_in = kwargs['expires_in']

            self.expiration = self.curr_time + timedelta(seconds=self.expires_in)
            self._id = kwargs['_id']
        except:
            pass

    meta = {
        'collection': 'tokens',
    }

    access_token = StringField()
    expiration = DateTimeField()
    expires_in = IntField()
    refresh_token = StringField()
    scope = StringField()
    token_type = StringField()
    _id = ObjectIdField()

    def save(self, **kwargs):
        super(Tokens, self).save()

    def update(self, kwargs):
        try:
            self.access_token = kwargs['access_token']
            self.token_type = kwargs['token_type']
            self.expires_in = kwargs['expires_in']
            self.scope = kwargs['scope']
        except:
            pass

    def _to_log_param(self):
        return {
            'access_token': str(self.access_token),
            'refresh_token': str(self.refresh_token),
            'expiration': str(self.expiration),  # javascript sucks, kibana won't render the Long correctly, must use str()
        }

    def __str__(self):
        return json.dumps(self._to_log_param())


def _get_token():
    tokens_collection = client[settings.DB][settings.TOKENS_COLLECTION]
    return tokens_collection.find_one()


def is_token_valid():
    token = _get_token()
    return datetime.now() < token['expiration']


def get_refresh_token():
    token = _get_token()
    return token['refresh_token']


def get_access_token():
    token = _get_token()
    return token['access_token']


def get_token_type():
    token = _get_token()
    return token['token_type']


def get_token():
    return Tokens(_get_token())


def has_token():
    return Tokens.objects.count() > 0
