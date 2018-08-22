from flask import Flask

from server.app import blueprint
from server.routes.spotify_auth import auth_blueprint
from server.routes.playlists import playlists_blueprint
from server.routes.tracks import tracks_blueprint, socket_io


app = Flask(__name__)

app.register_blueprint(blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(playlists_blueprint)
app.register_blueprint(tracks_blueprint)

socket_io.init_app(app)
