from marshmallow import Schema, fields


class GetPlaylistSchema(Schema):
    id = fields.Str()
    href = fields.Str()