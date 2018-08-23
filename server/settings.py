API_URL_BASE = 'https://api.spotify.com/v1/{endpoint}'
API_GET_PLAYLIST = API_URL_BASE.format(endpoint='users/theseanathan/playlists/{id}')

DB = 'pp'
TRACKS_COLLECTION = 'tracks'
TOKENS_COLLECTION = 'tokens'

DEFAULT_IMAGE = {
    'url': 'http://via.placeholder.com/60x60',
    'height': 60,
    'width': 60
}
