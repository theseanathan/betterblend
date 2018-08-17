import json
import requests

from server.lib import tokens
from server.lib.log import log

PLAYLIST_NAME = 'playlist_{}'


class SpotifyCallException(Exception):
    pass


headers = {'Authorization': 'Bearer {}'.format(tokens.get_access_token())}


def get(href: str):
    log.info('Calling spotify API')
    response = requests.get(href, headers=headers)

    if response.status_code != 200:
        raise SpotifyCallException('Spotify request failed with the status code: {}'.format(response.status_code))
    else:
        return json.loads(response.text)
