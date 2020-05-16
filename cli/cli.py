from typing import Any
from typing import Dict
from typing import List
import json
import random
import requests
import string
import urllib.parse as urllib
import webbrowser

from server import client_info

from pprint import pprint
from PyInquirer import prompt


def login():
    redirect_uri = 'http://localhost:5000/callback'
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
    redirect_str = url + urllib.urlencode(auth_dict)
    webbrowser.open(redirect_str)


def validate() -> bool:
    res = requests.get('http://localhost:5000/validate')
    if res.status_code == 200:
        return res.text == 'SUCCESS'
    return False


def get_playlists() -> List[Dict[Any, Any]]:
    playlists_response = requests.get('http://localhost:5000/get_playlists')
    playlists_obj = json.loads(playlists_response.text)

    return playlists_obj


if __name__ == '__main__':
    if not validate():
        login()

    print('API Validation successful')

    # TODO: Print directions for playlists

    playlists = get_playlists()
    playlist_question = [
        {
            'type': 'list',
            'name': 'playlist',
            'message': 'Which playlist do you want to sort?',
            'choices': playlists.keys()
        },
    ]

    answers = prompt(playlist_question)
    pprint(answers)
