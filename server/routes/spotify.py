from flask import Blueprint, request, jsonify
from webargs.flaskparser import use_args
import requests

from server import settings
from server.lib import tokens
from server.lib import spotify
from server.models.playlist import Playlist
from server.schemas.spotify import GetPlaylistSchema

spotify_blueprint = Blueprint('spotify', __name__)


class Spotify:
    @spotify_blueprint.route('/get_playlists', methods=['GET'])
    def get_playlists():
        """
        Gets playlists in Spotify acount.

        :return: List of playlist objects.
        [{
            'href': HREF,
            'id': ID,
            'image': {
                'height': HEIGHT,
                'width': WIDTH,
                'url': IMAGE_URL
            },
            'name': NAME
        }, ...]
        """
        get_playlist_endpoint = 'me/playlists'
        response = spotify.get(settings.API_URL_BASE.format(endpoint=get_playlist_endpoint))
        playlists_data = response['items']
        playlists = []
        for playlist_item in playlists_data:
            playlist = Playlist(playlist_item)
            playlist.get_tracks()
            playlists.append(str(playlist))

        return jsonify(playlists)

    @spotify_blueprint.route('/get_playlist', methods=['GET'])
    @use_args(GetPlaylistSchema, locations=['querystring'])
    def get_playlist(req):
        """
        Use schema get ID and href of playlist to get.

        :return: List of track object jsons
        """
        id = req.get('id')

        try:
            return jsonify(spotify.get_tracks(id))
        except Exception as e:
            return str(e)

    @spotify_blueprint.route('/vote_track', methods=['PUT'])
    def vote_track(self):
        pass

    @spotify_blueprint.route('/add_track', methods=['POST'])
    def add_track(self):
        pass
