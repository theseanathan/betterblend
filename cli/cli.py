import random
import requests
import string
import urllib.parse as urllib
import webbrowser

from server import client_info


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


if __name__ == '__main__':
    login()

    if not validate():
        raise Exception('Token validation failed.')

    print('API Validation successful')
