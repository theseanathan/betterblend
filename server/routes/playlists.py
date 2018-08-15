from flask import Blueprint, jsonify

from server import settings
from server.lib import spotify
from server.models.playlist import Playlist
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
        get_playlist_endpoint = 'me/playlists'
        response = spotify.get(settings.API_URL_BASE.format(endpoint=get_playlist_endpoint))
        playlists_data = response['items']

        playlist_schema = PlaylistSchema()
        playlists_schema = GetPlaylistSchema()
        playlists = {'playlists': []}

        for playlist_item in playlists_data:
            playlist = Playlist(playlist_item)
            playlist.get_tracks()

            playlist_data, error = playlist_schema.dump(playlist)
            playlists['playlists'].append(playlist_data)

        playlists_response, error = playlists_schema.dump(playlists)

        return jsonify(playlists_response)
