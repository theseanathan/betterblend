# BetterBlend Server

#### Server used to handle all logic related to Spotify pertinent data. 
Calls out to Spotify API to get information necessary for the web app and handles persistent storage using MongoDB. Saves track data and token data persistently. 

## API
### Playlists
`[GET] /get_playlists` Used to call out to Spotify and get the available playlists for the webapp. <br>
```
{
  playlists: [
    {
      href: str,
      id: str,
      name: str,
      image: {
		url: str,
        height: int,
        width: int
      }
    },
    ...
  ]
}
```

### Tracks
`[GET] /get_tracks` Used to get tracks of a particular playlist. <br>
Request: `id` of playlist as querystring param <br>
Response:
```
{
  tracks: [
    {
      artist: str,
      name: str,
      playlist_id: str,
      track_id: str,
      vote_count: int,
      voter_list: list[str]
    }, 
  	...
  ]
}
```
<br>
`[PUT] /vote_track` Up or down votes a particular track in the playlist. <br>
Request: `track_id [str]`, `playlist_id [str]` and `vote [int]` <br>
TODO: Possibly rather than use track_id and playlist_id, just using the Mongo document ObjectId
