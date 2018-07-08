from mongoengine import (
    connect,
    Document,
    FloatField,
    IntField,
    ListField,
    MapField,
    ObjectIdField,
    StringField,
    DictField,
    BooleanField,
)
from bson.objectid import ObjectId
import json
import requests

from server import settings
from server.lib import tokens

connect(settings.DB)


class TrackException(Exception):
    pass


class Track(Document):
    meta = {'collection': 'tracks'}

    def __init__(self, *args, **kwargs):
        super(Track, self).__init__(**kwargs)

        try:
            self.id = ObjectId()
            self.album = kwargs['album']
            self.artist = kwargs['artists'][0]['name']
            self.href = kwargs['href']
            self.name = kwargs['name']
            self.track_id = kwargs['id']
            self.voter_list = []
            self.vote_count = 0

            self.playlist_id = kwargs['playlist_id']
        except Exception as e:
            print("Track object creation failed: ", e)


    id = ObjectIdField(primary_key=True)
    album = StringField()
    artist = StringField()
    href = StringField()
    name = StringField()
    playlist_id = StringField()
    track_attributes = MapField(field=FloatField())
    track_id = StringField()
    voter_list = ListField(StringField())
    vote_count = IntField()

    artists = ListField()
    available_markets = ListField(StringField())
    disc_number = IntField()
    duration_ms = IntField()
    episode = BooleanField()
    explicit = BooleanField()
    external_fields = DictField()
    external_ids = DictField()
    external_urls = DictField()
    is_local = BooleanField()
    popularity = FloatField()
    preview_url = StringField()
    track = BooleanField()
    track_number = IntField()
    type = StringField()
    uri = StringField()

    def to_log(self):
        dict = {
            'artist': self.artist,
            'danceability': self.track_attributes['danceability'],
            'liveness': self.track_attributes['liveness'],
            'name': self.name,
            'playlist_id': self.playlist_id,
            'tempo': self.track_attributes['tempo'],
            'track_id': str(self.track_id),
            'voter_list': self.voter_list,
            'vote_count': self.vote_count,
        }
        return dict

    def pre_save(self):
        if self.playlist_id is None:
            raise TrackException('Every track needs to have a playlist_id')
        self._add_audio_analysis()

    def save(self, **kwargs):
        self.pre_save()
        super(Track, self).save()

    def _add_audio_analysis(self):
        me_headers = {'Authorization': 'Bearer {}'.format(tokens.get_access_token())}
        response = requests.get(settings.API_URL_BASE.format(endpoint='audio-features/{id}'.format(id=self.track_id)),
                                headers=me_headers)

        audio_analysis_info = json.loads(response.text)

        if 'danceability' in audio_analysis_info.keys():
            self.track_attributes['danceability'] = audio_analysis_info['danceability']
        if 'liveness' in audio_analysis_info.keys():
            self.track_attributes['liveness'] = audio_analysis_info['liveness']
        if 'tempo' in audio_analysis_info.keys():
            self.track_attributes['tempo'] = audio_analysis_info['tempo']
