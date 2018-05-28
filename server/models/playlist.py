from typing import List
import requests
import json

from models import tokens
from models.track import Track
import settings as settings


class Playlist:
    def __init__(self, **kwargs):
        self.href = kwargs['href']
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.tracks = [item.track for item in kwargs['tracks']['items']]

    def to_log(self):
        dict = {
            'name': self.name,
            'id': self.id,
            'href': self.href
        }
        return dict

    def save(self):
        for track in self.tracks:
            href = track['href']
            access_token = tokens.get_access_token()

            me_headers = {'Authorization': 'Bearer {}'.format(access_token)}
            track_dict = requests.get(href, headers=me_headers)

            track_object = json.loads(track_dict.text)
            track = Track(track_object)
            track.save()
