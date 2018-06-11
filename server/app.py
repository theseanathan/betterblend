from flask import request, Blueprint
import requests
import json

from server import settings
from server.lib import spotify, tokens
from server.models.playlist import Playlist
from server.models.playlist_track import PlaylistTrack
from server.routes.spotify_auth import auth_blueprint

blueprint = Blueprint('app', __name__)


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
