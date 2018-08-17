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


class PutTrackInputSchema(GetPlaylistSchema):
    vote = fields.Int(required=True)
    id = fields.Str(required=True)


class GetTracksInputSchema(Schema):
    id = fields.Str(required=True)


class TrackSchema(Schema):
    artist = fields.Str()
    danceability = fields.Float()
    id = fields.Str()
    image = fields.Nested(ImageSchema)
    liveness = fields.Float()
    name = fields.Str()
    playlist_id = fields.Str()
    tempo = fields.Float()
    track_id = fields.Str()
    voter_list = fields.List(fields.Str())
    vote_count = fields.Int()


class GetTracksResponseSchema(Schema):
    tracks = fields.List(fields.Nested(TrackSchema))
