import requests
import json

from server.lib import tokens


class SpotifyCallException(Exception):
    pass


def get(href: str):
    access_token = tokens.get_access_token()

    me_headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(href, headers=me_headers)

    if response.status_code != 200:
        raise SpotifyCallException('Spotify request failed with the status code: {}'.format(response.status_code))
    else:
        return json.loads(response.text)


