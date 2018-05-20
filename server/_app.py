from flask import (
    Blueprint,
    Flask,
    jsonify,
    make_response,
    request,
)
from functools import update_wrapper
from typing import Dict, Any
from datetime import timedelta
from pymongo import collection
import json
import requests

from models.playlist import Playlist
from models.playlist_track import PlaylistTrack


app = Flask(__name__)
blueprint = Blueprint('spotify_api', __name__)

spotify_api_url_base = 'https://api.spotify.com/v1/{endpoint}'

access_token = None
refresh_token = None


def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def get_request(url: str, access_token: str):
    header = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(url, headers=header)
    return json.loads(response.text)


@blueprint.route('/get_playlists', methods=['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*')
def get_playlists(req: Dict[str, Any] = None):
    access_token = request.args.get('access_token')

    get_playlist_endpoint = 'me/playlists'
    url = spotify_api_url_base.format(endpoint=get_playlist_endpoint)

    playlists_data = get_request(url, access_token)

    playlists = []
    for playlist in playlists_data['items']:
        playlists.append(Playlist(playlist))

    return_dict = {
        'playlists': [playlist.to_log() for playlist in playlists],
        'count': len(playlists)
    }

    return jsonify(return_dict)


@blueprint.route('/get_tracks', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def get_tracks(req: Dict[str, Any]):
    href = req.get('href')
    id = req.get('id')
    name = req.get('name')
    token = req.get('access_token')

    me_headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(href, headers=me_headers)

    playlist_data = json.loads(response.text)
    playlist = Playlist(playlist_data)

    tracks = []
    for track in playlist.tracks['items']:
        tracks.append(_add_audio_analysis(PlaylistTrack(track).track, token))

    playlist.add_tracks(tracks)

    return_dict = {
        'tracks': [track.to_log() for track in tracks],
        'count': len(tracks)
    }

    return jsonify(return_dict)


def _add_audio_analysis(track, token):
    me_headers = {'Authorization': 'Bearer {}'.format(token)}
    audio_analysis_endpoint = 'audio-features/{id}'.format(id=track.id)
    response = requests.get(spotify_api_url_base.format(endpoint=audio_analysis_endpoint, headers=me_headers))

    audio_analysis_info = json.loads(response.text)
    if 'danceability' in audio_analysis_info.keys():
        track.danceability = audio_analysis_info['danceability']
    if 'liveness' in audio_analysis_info.keys():
        track.liveness = audio_analysis_info['liveness']
    if 'energy' in audio_analysis_info.keys():
        track.energy = audio_analysis_info['energy']
    if 'tempo' in audio_analysis_info.keys():
        track.tempo = audio_analysis_info['tempo']

    return track


@blueprint.route('/vote_track', methods=['POST'])
def vote_track(req: Dict[str, Any]):
    """
    Up/down votes track by ID

    :param req:
    :return:
    """
    pass


def add_to_playlist():
    """
    Adds top voted track in queue to real playlist

    :return:
    """
    pass


app.register_blueprint(blueprint)
