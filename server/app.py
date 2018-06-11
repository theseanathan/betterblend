from flask import request, Blueprint

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
