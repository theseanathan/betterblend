from datetime import datetime

from server import settings
from server.lib import client, tokens_collection
from server.models.tokens import Tokens
from server.routes import spotify_auth


def _get_token():
    return tokens_collection.find_one()


def is_token_valid():
    token = _get_token()
    if token:
        return datetime.now() < token['expiration']
    return False


def get_refresh_token():
    token = _get_token()
    return token['refresh_token']


def get_access_token():
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
