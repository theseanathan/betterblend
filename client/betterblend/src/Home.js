import React, { Component } from 'react';
import './css/playlist.css';
import axios from 'axios';
import {Link} from 'react-router-dom';

class Home extends Component {

	constructor() {
		super();
		this.state = {
			classnames: 'playlists',
			playlists: []
		}
	}

	componentDidMount() {
		this.getPlaylists();
	}

	getPlaylists = () => {
		axios.get('/get_playlists')
		.then(data => {
			let modPlaylists = data.data.playlists.map(function(p) {
				if(Object.keys(p.image).length === 0) {
					p.image = {"height":60, "width":60, "url":"http://via.placeholder.com/60x60"};
				} return p;
			}); this.setState({playlists: modPlaylists});
		});
	};

	render() {
        //console.log(this.state.playlists);
		return (
			<div className={this.state.classnames}>
				{this.state.playlists.map(p => 
					<Link to={'/playlist/'+p.playlist_id} className="playlist-link" key={p.id}>
						<div className="playlist-div">
							<div className="left-style">
                           	 	<img src={p.image.url} alt=""/>
							</div>
							<p className="playlist-title">{p.name}</p>
						</div>
					</Link>
				)}
			</div>
		);
	}
}

export default Home;
