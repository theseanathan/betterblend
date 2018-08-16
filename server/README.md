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
`[PUT] /vote_track` Up or down votes a particular track in the playlist. <br>
Request: `id [str]` which is the mongo_id, and `vote [int]` <br>
<br> <br>
`[GET] /get_tracks` Used to get tracks of a particular playlist. <br>
Request: `id` of playlist as querystring param <br>
Response:
```
{
  tracks: [
    {
      artist: str,
      id: str
      name: str,
      playlist_id: str,
      track_id: str,
      vote_count: int,
      voter_list: list[str],
    }, 
  	...
  ]
}
```
