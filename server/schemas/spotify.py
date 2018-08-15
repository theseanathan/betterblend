from marshmallow import Schema, fields


class GetPlaylistSchema(Schema):
    id = fields.Str(required=True)

class PutPlaylistSchema(GetPlaylistSchema):
    vote = fields.Int(required=True)
