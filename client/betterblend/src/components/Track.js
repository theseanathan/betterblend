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
            console.log('CONNECTED TO THE FLASK SOCKET!');
            socket.emit('connected', '12345', (response) => {
                console.log('EMITTED TO FLASK SOCKET!', response);
            })

            socket.on('playlist', (response) => {
                console.log('ON PLAYLIST EMIT!!: ', response);
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
			//console.log(data.data.tracks);
			this.setState({tracks: data.data.tracks});
		});
	};

	render() {
		//console.log('id: ', this.props.location.pathname.substring(10));
		return (
			<div className={this.state.classnames}>
				{this.state.tracks.map((p, i) => 
					<div className="track-container" key={p.track_id}>
						<div className="left-style">
							<img src={p.image.url} alt=""/>
						</div>
						<div className="track-data">
							<p className="song-title"><b>{p.name}</b></p>
							<p className="artist">{p.artist}</p>
						</div>
						<TrackForm trackInfo={p} index={i}/>
					</div>
				)}
			</div>
		);
	}
}

export default Track;