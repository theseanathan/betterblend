from flask import request, Blueprint, Flask
import requests
import json

from server.lib import tokens
from server.models.playlist import Playlist
from server.models.playlist_track import PlaylistTrack
from server.routes.spotify import spotify_blueprint
from server.routes.spotify_auth import auth_blueprint

app = Flask(__name__)
blueprint = Blueprint('app', __name__)


def get_playlist():
    id = requests.args.get('id')
    href = requests.args.get('href')
    access_token = tokens.get_access_token()

    # TODO: Return playlist collection from Mongo with updated songs
    me_headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(href, headers=me_headers)

    playlist_info = json.loads(response.text)
    playlist = Playlist(playlist_info)

    tracks = []
    for track in playlist.tracks['items']:
        tracks.append(add_audio_analysis(PlaylistTrack(track).track, access_token))
    for track in tracks:
        print(track.name, track.tempo, track.danceability)


def add_audio_analysis(track, access_token):
    me_headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(api_url_base.format(endpoint='audio-features/{id}'.format(id=track.id)),
                            headers=me_headers)

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


@blueprint.route('/sort_playlist')
def sort_playlist():
    tracks = request.args.get('tracks')
    token = request.args.get('token')
    href = request.args.get('href')
    href += '/tracks'


    for track in tracks:
        print(track)
    tracks.sort(key=lambda track:track.danceability, reverse=True)
    for track in tracks:
        print(track.name)

    return tracks

app.register_blueprint(blueprint)
app.register_blueprint(spotify_blueprint)
app.register_blueprint(auth_blueprint)
