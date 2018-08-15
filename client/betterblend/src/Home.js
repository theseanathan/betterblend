import React, { Component } from 'react';
import './css/playlist.css';
import axios from 'axios';

class Home extends Component {

	constructor() {
		super();
		this.state = {
			classnames: '',
			playlists: []
		}
	}

	componentDidMount() {
		this.getPlaylists();
	}

	getPlaylists = () => {
		axios.get('/api')
		.then(data => this.setState({playlists: data.data.playlists}));
	};

	render() {
		return (
			<div className={this.state.classnames}>
				{this.state.playlists.map(p => 
					<a href="/tracks" className="playlist-link" key={p.id}><div className="playlist-div">
						<div className="left-style">
							<img src={p.img} alt=""/>
						</div>
						<p className="playlist-title">{p.name}</p>
					</div></a>
				)}
			</div>
		);
	}
}

export default Home;
