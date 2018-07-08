import requests
import json

from server import settings
from server.lib import tokens, tracks_collection
from server.models.playlist import Playlist
from server.models.track import Track

PLAYLIST_NAME = 'playlist_{}'


class SpotifyCallException(Exception):
    pass


headers = {'Authorization': 'Bearer {}'.format(tokens.get_access_token())}

def get(href: str):
    access_token = tokens.get_access_token()

    response = requests.get(href, headers=headers)

    if response.status_code != 200:
        raise SpotifyCallException('Spotify request failed with the status code: {}'.format(response.status_code))
    else:
        return json.loads(response.text)

def _get_tracks_from_spotify(playlist_id):
    url = settings.API_GET_PLAYLIST.format(id=playlist_id)
    response = requests.get(url, headers=headers)

    playlist_info = json.loads(response.text)
    playlist = Playlist(playlist_info)

    tracks = []

    for track in playlist.tracks['items']:
        track_model = Track(track['track'])
        track_model.playlist_id = playlist_id
        tracks.append(track_model)

    return tracks

def get_tracks(id):
    spotify_tracks = _get_tracks_from_spotify(id)
    db_tracks = list(tracks_collection.find({'playlist_id': id}))
    db_track_ids = [db_track['track_id'] for db_track in db_tracks]

    for track in spotify_tracks:
        if track.track_id not in db_track_ids:
            track.save()


    db_tracks = list(tracks_collection.find({'playlist_id': id}))

    for db_track in db_tracks:
        id = db_track['_id']
        del db_track['_id']
        db_track['id'] = id

    tracks = [Track(db_track).to_log() for db_track in db_tracks]

    return tracks
