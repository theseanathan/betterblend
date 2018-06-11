from mongoengine import EmbeddedDocument

from server.models.track import Track
from server.models.user import User


class PlaylistTrack:
    def __init__(self, **kwargs):
        super(PlaylistTrack, self).__init__(**kwargs)
        self.added_at = kwargs['added_at']
        self.added_by = User(kwargs['added_by'])
        self.track = Track(kwargs['track'])

    @property
    def id(self):
        if self.track:
            return self.track.id
        return None

    @property
    def name(self):
        if self.track:
            return self.track.name
        return None

    def to_log(self):
        dict = {
            'name': self.track.name,
            'artist': self.track.artist,
            'danceability': self.track.danceability,
            'liveness': self.track.liveness,
            'tempo': self.track.tempo
        }
        return dict
