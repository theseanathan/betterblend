import requests
import json

from server.lib import tokens, mongo_db

PLAYLIST_NAME = 'playlist_{}'


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


def _get_tracks(id, href):
    access_token = tokens.get_access_token()
    playlist_name = PLAYLIST_NAME.format(id)
    playlist_in_db = playlist_name in mongo_db.list_collection_names()

    if playlist_in_db:
        # TODO: Call spotify and match tracks to collection
        pass
    else:
        # TODO: Create Playlist track by creating list of Track objects and saving
        pass

