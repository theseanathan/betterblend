import random
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
    # response = requests.get(url, params=auth_dict)
    redirect_str = url + urllib.urlencode(auth_dict)
    webbrowser.open(redirect_str)


if __name__ == '__main__':
    login()
