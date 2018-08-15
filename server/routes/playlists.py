from flask import Blueprint, jsonify

from server import settings
from server.lib import spotify
from server.models.playlist import Playlist

playlists_blueprint = Blueprint('playlists', __name__)


class Playlists:
    @playlists_blueprint.route('/get_playlists', methods=['GET'])
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
