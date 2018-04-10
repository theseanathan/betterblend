class Track():
    def __init__(self, kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.popularity = kwargs['popularity']
        self.uri = kwargs['uri']
        if 'is_playable' in kwargs.keys():
            self.is_playable = kwargs['is_playable']
        self.href = kwargs['href']
        self.artist = kwargs['artists'][0]['name']
        self.album = kwargs['album']['name']
        self.danceability = None
        self.energy = None
        self.liveness = None
        self.tempo = None
