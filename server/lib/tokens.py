from typing import Dict
from typing import Optional
from typing import Any
from datetime import datetime
import os
import json

from server.lib import client, tokens_collection
from server.models.tokens import Tokens


cwd = os.getcwd()


def _get_token() -> Dict[Optional[str], Optional[Any]]:
    with open(os.path.join(cwd, 'metadata/token.txt'), 'r') as infile:
        token_data = json.load(infile)
        return token_data
    return {}


def is_token_valid() -> str:
    token = _get_token()
    if token:
        return datetime.now() < datetime.strptime(token['expiration'], '%Y-%m-%d %H:%M:%S.%f')
    return False


def get_refresh_token():
    token = _get_token()
    if token:
        return token['refresh_token']
    raise Exception("No refresh token")


def get_access_token():
    token = _get_token()
    if token:
        return token['access_token']
    raise Exception("No refresh token")

def get_token_type():
    token = _get_token()
    return token['token_type']


def get_token():
    return Tokens(_get_token())


def has_token():
    return Tokens.objects.count() > 0
