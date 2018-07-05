from flask import (
    Blueprint,
    redirect,
    request
)
from webargs.flaskparser import use_args

from server.models.playlist import Playlist
from server.lib import spotify
from server.schemas.spotify_schema import SpotifyGetPlaylistSchema
from server import settings

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

        return str(playlists)

    @spotify_blueprint.route('/get_playlist', methods=['GET'])
    @use_args(SpotifyGetPlaylistSchema, locations=['querystring'])
    def get_playlist(req):
        """
        Use schema OR use requests.args.get to get ID and href of playlist to get.
        If playlist exists, get and compare with spotify playlist.
        If not, create playlist and populate with tracks from spotify.

        :return: List of track object jsons
        """
        if 'href' in req:
            response = spotify.get(req['href'])
        else:
            get_playlist_endpoint = 'users/theseanathan/playlists/{id}/tracks'.format(id=req['id'])
            response = spotify.get(settings.API_URL_BASE.format(endpoint=get_playlist_endpoint))
        tracks = response['items']['tracks']

        return str(response['items'])

    @spotify_blueprint.route('/vote_track', methods=['PUT'])
    def vote_track(self):
        pass

    @spotify_blueprint.route('/add_track', methods=['POST'])
    def add_track(self):
        pass
