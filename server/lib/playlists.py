from server import settings
from server.models.playlist import Playlist
from server.resources import spotify


def _get_playlists_from_spotify():
    get_playlist_endpoint = 'me/playlists'
    response = spotify.get(settings.API_URL_BASE.format(endpoint=get_playlist_endpoint))
    playlists_data = response['items']

    for playlist_item in playlists_data:
        playlist = Playlist(**playlist_item)
        playlist.new_save()


def get_playlists():
    _get_playlists_from_spotify()
    playlists = Playlist.objects()

    return playlists


def get_playlist_name(playlist_id: str):
    playlists = Playlist.objects(playlist_id=playlist_id)
    return playlists[0].name