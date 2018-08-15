import React, { Component } from 'react';
import '../css/playlist.css';
import axios from 'axios';
import 'font-awesome/css/font-awesome.min.css';

class Track extends Component {

	constructor() {
		super();
		this.state = {
			classnames: '',
			tracks: []
		}
	}

	componentDidMount() {
		this.getPlaylists();
	}

	getPlaylists = () => {
		axios.get('/api')
		.then(data => this.setState({tracks: data.data.tracks}));
	};

	render() {
		return (
			<div className={this.state.classnames}>
				{this.state.tracks.map(p => 
					<div className="track-container" key={p.id}>
						<div className="left-style">
							<img src={p.img} alt=""/>
						</div>
						<div className="track-data">
							<p className="song-title"><b>{p.name}</b></p>
							<p className="artist">{p.artist}</p>
						</div>
						<div className="song-data">
							<div className="vote-buttons"><a><i className="fa fa-caret-up fa-lg"></i></a></div>
							<div className="vote-buttons"><a><i className="fa fa-caret-down fa-lg"></i></a></div>
							<div><p className="count-num">{p.count}</p></div>
						</div>
					</div>
				)}
			</div>
		);
	}
}

export default Track;