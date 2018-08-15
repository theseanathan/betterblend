from flask import Blueprint, jsonify
from webargs.flaskparser import use_args

from server.lib import spotify
from server.schemas.spotify import GetPlaylistSchema, PutPlaylistSchema


tracks_blueprint = Blueprint('tracks', __name__)


class Tracks:
    @tracks_blueprint.route('/get_playlist', methods=['GET'])
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

    @tracks_blueprint.route('/vote_track', methods=['PUT'])
    @use_args(PutPlaylistSchema, locations=['querystring', 'json'])
    def vote_track(req):
        """
        Vote up/down track

        :return: Vote track response
        """
        id = req.get('id')
        vote = req.get('vote')

        try:
            return spotify.vote_track(id, vote)
        except Exception as e:
            return str(e)

    @tracks_blueprint.route('/add_track', methods=['POST'])
    def add_track(self):
        pass
