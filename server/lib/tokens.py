from datetime import datetime
from pymongo import MongoClient

from server.models.tokens import Tokens
from server.routes import spotify_auth
from server import settings


client = MongoClient('localhost', 27017)


def _get_token():
    tokens_collection = client[settings.DB][settings.TOKENS_COLLECTION]
    return tokens_collection.find_one()

def has_token():
    token = _get_token()
    if not token:
        return False
    return True


def is_token_valid():
    token = _get_token()
    if not has_token():
        return False
    return datetime.now() < token['expiration']


def get_refresh_token():
    token = _get_token()
    return token['refresh_token']


def get_access_token():
    if not has_token():
        spotify_auth.get_access_token()
    if not is_token_valid():
        spotify_auth.update_token()
    token = _get_token()
    return token['access_token']


def get_token_type():
    token = _get_token()
    return token['token_type']


def get_token():
    return Tokens(_get_token())


def has_token():
    return Tokens.objects.count() > 0
