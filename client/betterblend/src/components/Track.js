import React, { Component } from 'react';
import '../css/playlist.css';
import axios from 'axios';
import 'font-awesome/css/font-awesome.min.css';
import io from 'socket.io-client'

class Track extends Component {

	constructor() {
		super();
		this.state = {
			classnames: '',
			tracks: [
				{
				  'image': 'http://via.placeholder.com/60x60',
			      'artist': 'artist',
			      'id': 'dfjksdf',
			      'name': 'name-test',
			      'playlist_id': 'dffsd',
			      'track_id': 'dsfsf',
			      'vote_count': 69,
			      'voter_list': []
			    }
			]
		}

        const socket = io('http://localhost:5000')
        socket.on('connect', () => {
            socket.on('VOTED', (response) => {
                console.log('On \'VOTED\': ', response);
            })
        });
	}

	componentDidMount() {
		this.getTracks();
	}
	
	getTracks = () => {
		const trackUrl = '/get_playlist?id='+ this.props.location.pathname.substring(10);
		axios.get(trackUrl)
		.then(data => {
			let modTracks = data.data.tracks.map(function(t) {
				if(!('image' in t)) {
					t['image'] = "http://via.placeholder.com/60x60";
				} return t;
			}); this.setState({tracks: modTracks});
		});
	};

	render() {
		return (
			<div className={this.state.classnames}>
				{this.state.tracks.map(p => 
					<div className="track-container" key={p.track_id}>
						<div className="left-style">
							<img src={p.image.url} alt=""/>
						</div>
						<div className="track-data">
							<p className="song-title"><b>{p.name}</b></p>
							<p className="artist">{p.artist}</p>
						</div>
						<div className="song-data">
							<div className="vote-buttons"><a><i className="fa fa-caret-up fa-lg"></i></a></div>
							<div className="vote-buttons"><a><i className="fa fa-caret-down fa-lg"></i></a></div>
							<div><p className="count-num">{p.vote_count}</p></div>
						</div>
					</div>
				)}
			</div>
		);
	}
}

export default Track;
