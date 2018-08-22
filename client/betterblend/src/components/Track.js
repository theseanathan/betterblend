import React, { Component } from 'react';
import '../css/playlist.css';
import axios from 'axios';
import TrackForm from './Track_Form.js'
import 'font-awesome/css/font-awesome.min.css';
import io from 'socket.io-client'

class Track extends Component {

	constructor() {
		super();
		this.state = {
			classnames: '',
			tracks: []
		}

        const socket = io('http://localhost:5000')
        socket.on('connect', () => {
            socket.on('VOTED', (response) => {
                this.render();
            });
        });
	}

	componentDidMount() {
		this.getTracks();
	}
	
	getTracks = () => {
        const trackUrl = '/get_playlist?id='+ this.props.location.pathname.substring(10);
        axios.get(trackUrl)
        .then(data => {
            this.setState({tracks: data.data.tracks});
        });
	};

	render() {
		return (
			<div className={this.state.classnames}>
				{this.state.tracks.map((track, i) => 
					<div className="track-container" key={track.track_id}>
						<div className="left-style">
							<img src={track.image.url} alt=""/>
						</div>
						<div className="track-data">
							<p className="song-title"><b>{track.name}</b></p>
							<p className="artist">{track.artist}</p>
						</div>
						<TrackForm trackInfo={track} index={i}/>
					</div>
				)}
			</div>
		);
	}
}

export default Track;
