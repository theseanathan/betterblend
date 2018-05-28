from mongoengine import Document, StringField, IntField, ListField, MapField
import json
import requests

import settings
from models import tokens


class Track(Document):
    def __init__(self, **kwargs):
        super(Track, self).__init__(**kwargs)

        try:
            self.album = kwargs['album']['name']
            self.artist = kwargs['artists'][0]['name']
            self.href = kwargs['href']
            self.id = kwargs['id']
            self.name = kwargs['name']
            self.vote_count = 0
            self.voter_list = []
        except Exception as e:
            print("Track object creation failed: ", e)

        self.track_attributes['danceability'] = None
        self.track_attributes['liveness'] = None
        self.track_attributes['tempo'] = None

        self.meta['collection'] = 'playlist_{}'.format(self.id)

    album = StringField()
    artist = StringField()
    href = StringField()
    id = StringField()
    name = StringField()
    vote_count = IntField()
    voter_list = ListField(StringField())
    track_attributes = MapField(StringField())

    def to_log(self):
        dict = {
            'name': self.name,
            'artist': self.artist,
            'danceability': self.track_attributes['danceability'],
            'liveness': self.track_attributes['liveness'],
            'tempo': self.track_attributes['tempo'],
            'id': self.id,
            'vote_count': self.vote_count,
            'voter_list': self.voter_list
        }
        return dict

    def pre_save(self):
        self._add_audio_analysis()

    def save(self, **kwargs):
        self.pre_save()
        super(Track, self).save()

    def _add_audio_analysis(self):
        me_headers = {'Authorization': 'Bearer {}'.format(tokens.get_access_token())}
        response = requests.get(settings.API_URL_BASE.format(endpoint='audio-features/{id}'.format(id=self.id)),
                                headers=me_headers)

        audio_analysis_info = json.loads(response.text)
        if 'danceability' in audio_analysis_info.keys():
            self.track_attributes['danceability'] = audio_analysis_info['danceability']
        if 'liveness' in audio_analysis_info.keys():
            self.track_attributes['liveness'] = audio_analysis_info['liveness']
        if 'tempo' in audio_analysis_info.keys():
            self.track_attributes['tempo'] = audio_analysis_info['tempo']
