from server.models.user import User
from pymongo import MongoClient
from typing import List

from server.models.playlist_track import PlaylistTrack
import server.settings as settings


class Playlist():
    def __init__(self, kwargs):
        self.href = kwargs['href']
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.owner = User(kwargs['owner'])
        self.tracks = kwargs['tracks']
        self.uri = kwargs['uri']

        self.mongo_client = MongoClient('localhost', 27017)
        self.db = self.mongo_client[settings.DB]
        if self.id not in self.db.collection_names():
            self.db.create_collection(self.id)
        self.collection = self.db[self.id]

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
