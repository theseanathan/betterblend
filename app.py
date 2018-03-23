import client_info

from flask import Flask, Blueprint, request, redirect, url_for
import base64
import random
import requests
import string
import urllib

app = Flask(__name__)
blueprint = Blueprint('spotify_api', __name__)

redirect_uri = 'http://localhost:5000/callback'


@blueprint.route('/', methods=['GET'])
@blueprint.route('/login', methods=['GET'])
def login():
    print("WHAT THE FUCK")
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
    print("SENDING GET")
    # response = requests.get(url, params=auth_dict)
    return redirect(url + urllib.urlencode(auth_dict))


@blueprint.route('/callback', methods=['GET'])
def callback():
    url = 'https://accounts.spotify.com/api/token'
    code = request.args.get('code')
    state = request.args.get('state')
    if state is not None:
        b64_client = base64.b64encode('{}:{}'.format(client_info.CLIENT_ID, client_info.CLIENT_SECRET))
        print("ENCODED:        ", b64_client)
        print("DECODED:        ", base64.b64decode(b64_client))
        print("AUTHORIZATION:   Basic: {}".format(b64_client))
        token_header = {
            'Authorization': 'Basic {}'.format(b64_client),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # 'client_id': client_info.CLIENT_ID,
        # 'client_secret': client_info.CLIENT_SECRET,
        auth_dict = {
            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        # headers = base64.b64encode('{}:{}'.format(client_info.CLIENT_ID, client_info.CLIENT_SECRET))
        response = requests.post(url, data=auth_dict, headers=token_header, json=True)
        if response.status_code == 200:
            print response.request.body
            access_token = response.content
            me_url = 'https://api.spotify.com/v1/me'
            me_headers = {'Authorization': 'Bearer {}'.format(access_token)}
            response = requests.get(me_url, headers=me_headers, json=True)
            if response.status_code == 200:
                return redirect('/#')

    return response.text

app.register_blueprint(blueprint)
