from flask import (
    Blueprint,
    redirect,
    request
)

import base64
import json
import random
import requests
import string
import urllib.parse as urllib

from server import client_info
from server.lib import tokens
from server.models.tokens import Tokens

auth_blueprint = Blueprint('spotify_auth', __name__)

redirect_uri = 'http://localhost:5000/callback'
access_token = None
refresh_token = None


@auth_blueprint.route('/authorize', methods=['GET'])
def login():
    url = 'https://accounts.spotify.com/authorize?'
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
    scope = 'user-read-private user-read-email'
    auth_dict = {
        'client_id': client_info.CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'state': state,
        'scope': scope,
    }
    # response = requests.get(url, params=auth_dict)
    redirect_str = url + urllib.urlencode(auth_dict)
    return redirect(redirect_str)


@auth_blueprint.route('/callback', methods=['GET'])
def callback():
    print("CALLBACK")
    if not tokens.has_token():
        code = request.args.get('code')
        state = request.args.get('state')
        return first_time_save_token(code, state)
    else:
        return update_token()


def first_time_save_token(code, state):
    url = 'https://accounts.spotify.com/api/token'
    client = '{}:{}'.format(client_info.CLIENT_ID, client_info.CLIENT_SECRET).encode()
    if state is not None:
        b64_client = base64.b64encode(client).decode('ascii')
        token_header = {
            'Authorization': 'Basic {}'.format(b64_client)
        }
        auth_dict = {
            'code': code.encode('ascii'),
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        response = requests.post(url, data=auth_dict, headers=token_header)
        response_content = json.loads(response.content)
        if response.status_code == 200:
            token = Tokens(response_content)
            token.save()
            return token._to_log_param()
        else:
            raise Exception(response.text)


def update_token():
    if not tokens.is_token_valid():
        print("UPDATE_TOKEN")
        url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': tokens.get_refresh_token()
        }
        client = '{}:{}'.format(client_info.CLIENT_ID, client_info.CLIENT_SECRET).encode()
        b64_client = base64.b64encode(client).decode('ascii')
        token_header = {
            'Authorization': 'Basic {}'.format(b64_client)
        }
        response = requests.post(url, data=data, headers=token_header)
        print("AFTER API CALL")
        response_content = json.loads(response.content)

        token = tokens.get_token()
        token.update(response_content)
        print("AFTER UPDATE TOKEN")
        token.save()

        return str(token)
    else:
        token = tokens.get_token()
        return str(token)
