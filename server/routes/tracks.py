from flask import Blueprint, jsonify, make_response
from flask_socketio import SocketIO
from webargs.flaskparser import use_args

from server.lib import tracks
from server.lib.log import log
from server.schemas.spotify import (
    GetTracksInputSchema,
    GetTracksResponseSchema,
    PutTrackInputSchema,
    TrackSchema
)


tracks_blueprint = Blueprint('tracks', __name__)
socket_io = SocketIO()


class Tracks:
    @tracks_blueprint.route('/get_playlist', methods=['GET'])
    @use_args(GetTracksInputSchema, locations=['querystring'])
    def get_playlist(req):
        """
        Use schema get ID and href of playlist to get.

        :return: List of track object jsons
        """
        id = req.get('id')

        try:
            return jsonify(_get_tracks_obj(id))
        except Exception as e:
            log.exception('An exception occurred at the get_playlist endpoint.')
            return str(e)

    @tracks_blueprint.route('/vote_track', methods=['PUT'])
    @use_args(PutTrackInputSchema)
    def vote_track(req):
        """
        Vote up/down track
        id = mongo object id [str]
        vote = up/down vote [int]

        :return: Vote track response
        """
        id = req.get('id')
        vote = req.get('vote')

        try:
            playlist_id = tracks._get_track(id).playlist_id
            socket_io.emit('VOTED', _get_tracks_obj(playlist_id))
            return make_response(tracks.vote_track(id, vote), 200)
        except Exception as e:
            return make_response(str(e), 500)

    @tracks_blueprint.route('/add_track', methods=['POST'])
    def add_track(self):
        pass


def _get_tracks_obj(playlist_id):
    spotify_tracks = tracks.get_tracks(playlist_id)
    track_schema = TrackSchema()
    tracks_schema = GetTracksResponseSchema()
    tracks_obj = {'tracks': []}

    for track in spotify_tracks:
        track_data, error = track_schema.dump(track)
        tracks_obj['tracks'].append(track_data)

    tracks_response, error = tracks_schema.dump(tracks_obj)
    return tracks_response
