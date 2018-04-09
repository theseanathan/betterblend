import client_info
from models.playlist import Playlist
from models.track import Track
from models.playlist_track import PlaylistTrack

from flask import Flask, Blueprint, request, redirect, render_template
import base64
import random
import requests
import string
import urllib
import json

import pdb

app = Flask(__name__)
blueprint = Blueprint('spotify_api', __name__)

api_url_base = 'https://api.spotify.com/v1/{endpoint}'
redirect_uri = 'http://localhost:5000/callback'
access_token = None
refresh_token = None


@blueprint.route('/login', methods=['GET'])
def login():
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
    print("REDIRECTING TO: " + redirect_str)
    return redirect(redirect_str)


@blueprint.route('/callback', methods=['GET'])
def callback():
    url = 'https://accounts.spotify.com/api/token'
    code = request.args.get('code')
    state = request.args.get('state')
    if state is not None:
        b64_client = base64.b64encode('{}:{}'.format(client_info.CLIENT_ID, client_info.CLIENT_SECRET))
        token_header = {
            'Authorization': 'Basic {}'.format(b64_client)
        }
        auth_dict = {
            'code': code.encode('ascii'),
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        response = requests.post(url, data=auth_dict, headers=token_header, json=True)
        response_content = json.loads(response.content)
        access_token = response_content.get('access_token')
        refresh_token = response_content.get('refresh_token')

        if response.status_code == 200:
            return home(access_token)
        else:
            raise Exception(response)


def home(token):
    return render_template('index.html', token=token)


@blueprint.route('/get_playlists')
def get_playlists():
    get_playlist_endpoint = 'me/playlists'
    access_token = request.args.get('token')
    me_headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(api_url_base.format(endpoint=get_playlist_endpoint),
                            headers=me_headers,
                            json=True)
    playlists_data = json.loads(response.text)
    playlists = []
    for playlist in playlists_data['items']:
        playlists.append(Playlist(playlist))
    playlist_info_list = []
    """
    for playlist in playlists:
        playlist_info_list.append(get_playlist(playlist.href, access_token))
    """
    return render_template('playlists.html', playlists=playlists, token=access_token)


@blueprint.route('/get_playlist')
def get_playlist():
    href = request.args.get('href')
    access_token = request.args.get('token')

    me_headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(href, headers=me_headers, json=True)

    playlist_info = json.loads(response.text)
    playlist = Playlist(playlist_info)

    tracks = []
    for track in playlist.tracks['items']:
        tracks.append(add_audio_analysis(PlaylistTrack(track).track, access_token))
    for track in tracks:
        print(track.name, track.tempo, track.danceability)

    return render_template('playlist_tracks.html', tracks=tracks, token=access_token, playlist=playlist)


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
        print track
    tracks.sort(key=lambda track:track.danceability, reverse=True)
    for track in tracks:
        print(track.name)

    return tracks


app.register_blueprint(blueprint)
