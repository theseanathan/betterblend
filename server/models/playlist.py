from bson.objectid import ObjectId
from mongoengine import (
    Document,
    StringField,
    ObjectIdField,
    DictField,
    BooleanField,
    ListField,
)

from server import settings


class Playlist(Document):
    meta = {'collection': 'playlists'}

    collaborative = BooleanField()
    external_urls = DictField()
    href = StringField()
    id = ObjectIdField(primary_key=True)
    image = DictField()
    images = ListField(DictField())
    name = StringField()
    owner = DictField()
    playlist_id = StringField()
    primary_color = StringField()
    public = BooleanField()
    snapshot_id = StringField()
    tracks = DictField()
    type = StringField()
    uri = StringField()

    def __init__(self, *args, **kwargs):
        super(Playlist, self).__init__(**kwargs)

        try:
            self.href = kwargs['href']
            self.id = kwargs['id'] if 'playlist_id' in kwargs else ObjectId()
            self.images = kwargs['images']
            self.image = None
            self.name = kwargs['name']
            self.playlist_id = kwargs['playlist_id'] if 'playlist_id' in kwargs else kwargs['id']

            for img in self.images:
                if img['height'] == 60:
                    self.image = img
        except Exception as e:
            print("No item attribute, ", e)

    def set_image(self, image_obj):
        self.image = image_obj

    def pre_save(self):
        if not self.image:
            self.set_image(settings.DEFAULT_IMAGE)

    def exists(self):
        if Playlist.objects(playlist_id=self.playlist_id):
            return True
        return False

    def save(self):
        self.pre_save()
        super(Playlist, self).save()

    def new_save(self):
        if not self.exists():
            self.save()

    def to_log(self):
        dict = {
            'href': self.href,
            'id': self.playlist_id,
            'image': self.image,
            'mongo_id': self.id,
            'name': self.name,
        }
        return dict

    def __str__(self):
        return str(self.to_log())
