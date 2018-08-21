from server import settings
from server.resources import spotify
from server.lib.log import log
from server.models.playlist import Playlist
from server.models.track import Track


def _get_tracks_from_spotify(playlist_id):
    log.info('Getting tracks from spotify.')
    url = settings.API_GET_PLAYLIST.format(id=playlist_id)
    response = spotify.get(url)

    tracks = []

    for track in response['tracks']['items']:
        track['track']['playlist_id'] = playlist_id
        track['track']['album'] = track['track']['album']['name']

        track_model = Track(**track['track'])
        tracks.append(track_model)

    return tracks


def get_tracks(id):
    spotify_tracks = _get_tracks_from_spotify(id)
    _add_tracks_to_mongo(spotify_tracks, id)

    tracks = Track.objects(playlist_id=id)

    return tracks


def _add_tracks_to_mongo(tracks, playlist_id):
    log.info('Adding spotify tracks to db.')
    db_tracks = Track.objects(playlist_id=playlist_id)

    for track in tracks:
        if track not in db_tracks:
            try:
                track.new_save()
            except Exception as e:
                log.exception("Exception thrown when saving track to Mongo.")
                log.info('Track failed: {}'.format(track.track_id))


def _get_track(mongo_id):
    try:
        track = Track.objects.get(id=mongo_id)
        return track
    except Track.DoesNotExist as e:
        log.exception('Track does not exist.')
    except Exception as e:
        log.exception("Exception was thrown when getting track from Mongo.")
        log.info('Track failed: {}'.format(track.id))


# TODO: Add a unique user account to add to voters_list for track s.t. people can't vote twice
def vote_track(mongo_id, vote):
    try:
        track = _get_track(mongo_id)
        track.vote_count += vote
        track.save()
    except:
        raise
