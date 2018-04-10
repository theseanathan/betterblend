from models.track import Track
from models.user import User


class PlaylistTrack():
    def __init__(self, kwargs):
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