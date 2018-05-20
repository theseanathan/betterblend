from models.user import User
from mongoengine import Document, StringField, EmbeddedDocumentField, ListField
from pymongo import MongoClient
from typing import List

from models.playlist_track import PlaylistTrack
import settings as settings


class Playlist(Document):
    def __init__(self, **kwargs):
        super(Playlist, self).__init__(**kwargs)
        self.href = kwargs['href']
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.owner = User(kwargs['owner'])
        self.tracks = kwargs['tracks']
        self.uri = kwargs['uri']

        self.meta['collection'] = 'playlist_{}'.format(self.id)

    href = StringField()
    id = StringField()
    name = StringField()
    owner = EmbeddedDocumentField(User)
    tracks = ListField(EmbeddedDocumentField(PlaylistTrack))
    uri = StringField()

    def to_log(self):
        dict = {
            'name': self.name,
            'id': self.id,
            'href': self.href
        }
        return dict

    def add_tracks(self, tracks: List[PlaylistTrack]):
        self.tracks = tracks

    def save(self):
        for track in self.tracks:
            self.collection.insert_one(track.to_log())
