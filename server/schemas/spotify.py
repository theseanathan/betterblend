from marshmallow import Schema, fields


class ImageSchema(Schema):
    height = fields.Int()
    url = fields.Str()
    width = fields.Int()


class PlaylistSchema(Schema):
    href = fields.Str()
    id = fields.Str()
    image = fields.Nested(ImageSchema)
    name = fields.Str()


class GetPlaylistSchema(Schema):
    playlists = fields.List(fields.Nested(PlaylistSchema))


class PutPlaylistSchema(GetPlaylistSchema):
    vote = fields.Int(required=True)
