from flask import make_response
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
        track['track']['playlist_id'] = playlist_id
        track['track']['album'] = track['track']['album']['name']
        track_model = Track(**track['track'])
        tracks.append(track_model)

    return tracks


def get_tracks(id):
    spotify_tracks = _get_tracks_from_spotify(id)
    _add_tracks_to_mongo(spotify_tracks, id)

    tracks = [track.to_log() for track in Track.objects(playlist_id=id)]

    return tracks


def _add_tracks_to_mongo(tracks, playlist_id):
    db_tracks = Track.objects(playlist_id=playlist_id)

    for track in tracks:
        if track not in db_tracks:
            try:
                track.save()
            except Exception as e:
                print(str(e))


def vote_track(track_id, playlist_id, vote):
    track = Track.objects.get(track_id=id, playlist_id=playlist_id)
    track.vote_count = track.vote_count + vote
    track.save()
    return make_response('Vote successful!', 200)
