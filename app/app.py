import client_info

from flask import Flask, Blueprint, request, redirect
import base64
import random
import requests
import string
import urllib
import json

app = Flask(__name__)
blueprint = Blueprint('spotify_api', __name__)

api_url_base = 'https://api.spotify.com/v1/{endpoint}'
redirect_uri = 'http://localhost:5000/callback'


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
    if state is not None:
        b64_client = base64.b64encode('{}:{}'.format(client_info.CLIENT_ID, client_info.CLIENT_SECRET))
        token_header = {
            'Authorization': 'Basic {}'.format(b64_client)
        }
        auth_dict = {
            'code': code.encode('ascii'),
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        response = requests.post(url, data=auth_dict, headers=token_header, json=True)

        if response.status_code == 200:
            return response
        else:
            raise Exception(response)

def get_playlists(auth_response):
    response_content = json.loads(auth_response.content)

    access_token = response_content.get('access_token')
    refresh_token = response_content.get('refresh_token')

    get_playlist_endpoint = 'me/playlists'
    me_headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(api_url_base.format(endpoint=get_playlist_endpoint),
                            headers=me_headers,
                            json=True)
    return json.loads(response.text)

app.register_blueprint(blueprint)
