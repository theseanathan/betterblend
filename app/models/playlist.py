from models.user import User

class Playlist():
    def __init__(self, kwargs):
        self.href = kwargs['href']
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.owner = User(kwargs['owner'])
        self.tracks = kwargs['tracks']
        self.uri = kwargs['uri']
