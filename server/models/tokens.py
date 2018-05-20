from mongoengine import Document, StringField, DateTimeField

import settings

class Tokens:
    def __init__(self, **kwargs):
        super(Tokens, self).__init__(**kwargs)
        access_token = None
        refresh_token = None

    meta = {
        'collection': 'tokens',
    }

    access_token = StringField()
    expiration = DateTimeField()
    refresh_token = StringField()
    scope = StringField()
    token_type = StringField()
