from flask import Blueprint, request, jsonify
import requests

from server import settings
from server.lib import tokens
from server.lib import spotify
from server.models.playlist import Playlist

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
    def get_playlist():
        """
        Use schema OR use requests.args.get to get ID and href of playlist to get.
        If playlist exists, get and compare with spotify playlist.
        If not, create playlist and populate with tracks from spotify.

        :return: List of track object jsons
        """
        id = request.args.get('id')
        href = request.args.get('href')

        print('id: ', id, 'href', href)

        try:
            return jsonify(spotify.get_tracks(id, href))
        except:
            pass

    @spotify_blueprint.route('/vote_track', methods=['PUT'])
    def vote_track(self):
        pass

    @spotify_blueprint.route('/add_track', methods=['POST'])
    def add_track(self):
        pass
