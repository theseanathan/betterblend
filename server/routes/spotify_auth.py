from flask import (
    Blueprint,
    redirect,
    request
)

import base64
import random
import requests
import string
import urllib.parse as urllib

import client_info

blueprint = Blueprint('spotify_auth', __name__)

api_url_base = 'https://api.spotify.com/v1/{endpoint}'
redirect_uri = 'http://localhost:5000/callback'
access_token = None
refresh_token = None


@blueprint.route('/authorize', methods=['GET'])
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


@blueprint.route('/callback', methods=['GET'])
def callback():
    url = 'https://accounts.spotify.com/api/token'
    code = request.args.get('code')
    state = request.args.get('state')
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
        access_token = response_content.get('access_token')
        refresh_token = response_content.get('refresh_token')
        expiration = response_content.get('expiration')

        if response.status_code == 200:
            # return home(access_token)
            _save_tokens(access_token, refresh_token, expiration)
        else:
            raise Exception(response.text)

def _save_tokens(access_token: str, refresh_token: str, expiration: str):

