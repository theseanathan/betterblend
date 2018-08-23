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
                'id': ID,
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
        playlist_schema = PlaylistSchema()
        playlists_schema = GetPlaylistSchema()
        playlists_obj = {'playlists': []}

        playlist_docs = playlists.get_playlists()

        for playlist in playlist_docs:
            playlist_data, error = playlist_schema.dump(playlist)
            playlists_obj['playlists'].append(playlist_data)

        playlists_response, error = playlists_schema.dump(playlists_obj)

        return jsonify(playlists_response)
