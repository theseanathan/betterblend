from flask import (
    Blueprint,
    redirect,
    request
)

import base64
import json
import requests
import os

from server import client_info
from server.lib import tokens
from server.models.tokens import Tokens

auth_blueprint = Blueprint('spotify_auth', __name__)

redirect_uri = 'http://localhost:5000/callback'
cwd = os.getcwd()
access_token = None
refresh_token = None


@auth_blueprint.route('/callback', methods=['GET'])
def callback():
    print("CALLBACK")

    code = request.args.get('code')
    state = request.args.get('state')
    print(f'code: {code}')
    print(f'state: {state}')

    token_data = {
        'code': code,
        'state': state
    }

    with open(os.path.join(cwd, 'metadata/token.txt'), 'w') as outfile:
        json.dump(token_data, outfile)

    return first_time_save_token(code, state)

@auth_blueprint.route('/validate', methods=['GET'])
def validate():
    with open(os.path.join(cwd, 'metadata/token.txt'), 'r') as readfile:
        token_data = json.load(readfile)
        if 'access_token' in token_data:
            return 'SUCCESS'
        return 'FAILURE'

    raise Exception('Token file open fail')


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
            with open(os.path.join(cwd, 'metadata/token.txt'), 'w') as outfile:
                json.dump(response_content, outfile)
            return 'SUCCESS'
        else:
            raise Exception(response.text)
