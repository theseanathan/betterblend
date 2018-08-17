import json
import logging
import requests
import sys

from server.lib import tokens

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter('[%(levelname)s]|[%(name)s - %(asctime)s]: %(message)s'))

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

log.addHandler(ch)

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


