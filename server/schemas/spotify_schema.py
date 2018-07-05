from marshmallow import Schema, fields


class SpotifyGetPlaylistSchema(Schema):
    id = fields.Str()
    href = fields.Str()