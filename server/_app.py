from flask import Flask, Blueprint, request, redirect, render_template
import json
import requests
from typing import Dict, Any
import urllib.parse as urllib

from server.models.playlist import Playlist
from server.models.playlist_track import PlaylistTrack


app = Flask(__name__)
blueprint = Blueprint('spotify_api', __name__)

redirect_uri = 'http://localhost:5000/callback'
spotify_api_url_base = 'https://api.spotify.com/v1/{endpoint}'

access_token = None
refresh_token = None


@blueprint.route('/get_playlists', methods=['GET'])
def get_playlists(req: Dict[str, Any]):
    get_playlist_endpoint = 'me/playlists'
    access_token = req.get('token')
    # TODO: DECODE ACCESS TOKEN

    me_headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(spotify_api_url_base.format(endpoint=get_playlist_endpoint),
                            headers=me_headers)

    playlists_data = json.loads(response.text)

    playlists = []
    for playlist in playlists_data['items']:
        playlists.append(Playlist(playlist))

    return_dict = {
        'playlists': [playlist.to_log() for playlist in playlists],
        'count': len(playlists)
    }

    return return_dict


@blueprint.route('/get_tracks', methods=['GET'])
def get_tracks(req: Dict[str, Any]):
    href = req.get('href')
    token = req.get('token')

    me_headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(href, headers=me_headers)

    playlist_data = json.loads(response.text)
    playlist = Playlist(playlist_data)

    tracks = []
    for track in playlist.tracks['items']:
        tracks.append(_add_audio_analysis(PlaylistTrack(track).track, token))

    return_dict = {
        'tracks': [track.to_log() for track in tracks],
        'count': len(tracks)
    }

    return return_dict


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
