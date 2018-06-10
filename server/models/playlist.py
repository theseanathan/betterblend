import requests
import json

from server.lib import spotify
from server.lib import tokens
from server.models.track import Track


class Playlist:
    def __init__(self, kwargs):
        try:
            self.href = kwargs['href']
            self.id = kwargs['id']
            self.name = kwargs['name']
            self.image = kwargs['images']
            self.tracks = None

            for img in self.image:
                if img['height'] == 60:
                    self.image = img
        except Exception as e:
            print("No item attribute, ", e)

    def to_log(self):
        dict = {
            'href': self.href,
            'id': self.id,
            'image': self.image,
            'name': self.name,
        }
        return dict

    def __str__(self):
        return str(self.to_log())

    def get_tracks(self):
        playlist_info = spotify.get(self.href)
        self.tracks = playlist_info['tracks']['items']

    def save(self):
        for track in self.tracks:
            href = track['href']
            access_token = tokens.get_access_token()

            me_headers = {'Authorization': 'Bearer {}'.format(access_token)}
            track_dict = requests.get(href, headers=me_headers)

            track_object = json.loads(track_dict.text)
            track = Track(track_object)
            track.save()
