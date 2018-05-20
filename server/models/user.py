from mongoengine import EmbeddedDocument


class User(EmbeddedDocument):
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        if kwargs:
            if 'display_name' in kwargs.keys():
                self.display_name = kwargs['display_name']
            self.href = kwargs['href']
            self.id = kwargs['id']
            self.uri = kwargs['uri']