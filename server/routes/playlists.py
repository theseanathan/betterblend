from flask import Blueprint, jsonify

from server import settings
from server.resources import spotify
from server.models.playlist import Playlist
from server.lib import playlists
from server.schemas.spotify import PlaylistSchema, GetPlaylistSchema

playlists_blueprint = Blueprint('playlists', __name__)


class Playlists:
    @playlists_blueprint.route('/get_playlists', methods=['GET'])
    def get_playlists():
        """
        Gets playlists in Spotify acount.

        :return: List of playlist objects.
        {
            'playlists': [
            {
                'href': HREF,
                'tracks': {href, size},
                'image': {
                    'height': HEIGHT,
                    'width': WIDTH,
                    'url': IMAGE_URL
                },
                'name': NAME
            },
            ...]
        }
        """
        playlists_obj = {}

        playlist_docs = playlists.get_playlists()

        for playlist in playlist_docs:
            playlists_obj[playlist['name']] = playlist

        return jsonify(playlists_obj)
