from flask import make_response
import json
import logging
import requests
import sys

from server import settings
from server.lib import tokens
from server.models.playlist import Playlist
from server.models.track import Track

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
    response = requests.get(href, headers=headers)

    if response.status_code != 200:
        raise SpotifyCallException('Spotify request failed with the status code: {}'.format(response.status_code))
    else:
        return json.loads(response.text)


def _get_tracks_from_spotify(playlist_id):
    log.info('Getting tracks from spotify.')
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

    tracks = Track.objects(playlist_id=id)

    return tracks


def _add_tracks_to_mongo(tracks, playlist_id):
    log.info('Adding spotify tracks to db.')
    db_tracks = Track.objects(playlist_id=playlist_id)

    for track in tracks:
        if track not in db_tracks:
            try:
                track.save()
            except Exception as e:
                log.info("Exception thrown when saving track", exception=e)


def _get_track(track_id, playlist_id):
    try:
        tracks = Track.objects(playlist_id=playlist_id)
        tracks = [track for track in tracks if track.track_id == track_id]
        if len(tracks) <= 0:
            raise Track.DoesNotExist("track: {track}, playlist: {playlist}".format(track=track_id,
                                                                                   playlist=playlist_id))
        else:
            return tracks[0]
    except Track.DoesNotExist as e:
        log.info('Track does not exist.')
    except Exception as e:
        log.info("Exception was thrown when getting track from Mongo.", e)



def vote_track(track_id, playlist_id, vote):
    track = _get_track(track_id, playlist_id)
    track.vote_count = track.vote_count + vote
    track.save()
    return make_response('Vote successful!', 200)
