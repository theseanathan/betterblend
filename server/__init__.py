from flask import Flask


from server.app import blueprint
from server.routes.spotify_auth import auth_blueprint
from server.routes.spotify import spotify_blueprint


app = Flask(__name__)

app.register_blueprint(blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(spotify_blueprint)
