class Track():
    def __init__(self, kwargs):
        self.album = kwargs['album']['name']
        self.artist = kwargs['artists'][0]['name']
        self.danceability = None
        self.energy = None
        self.href = kwargs['href']
        self.id = kwargs['id']
        self.liveness = None
        self.name = kwargs['name']
        self.popularity = kwargs['popularity']
        self.tempo = None
        self.uri = kwargs['uri']
        self.vote_count = 0
        self.voter_list = []
        if 'is_playable' in kwargs.keys():
            self.is_playable = kwargs['is_playable']

    def to_log(self):
        dict = {
            'name': self.name,
            'artist': self.artist,
            'danceability': self.danceability,
            'liveness': self.liveness,
            'tempo': self.tempo,
            'id': self.id,
            'vote_count': self.vote_count,
            'voter_list': self.voter_list
        }
        return dict
