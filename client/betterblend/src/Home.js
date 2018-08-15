import React, { Component } from 'react';
import './css/playlist.css';
import axios from 'axios';
import _ from 'lodash';

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
		.then(data => this.setState({playlists: data.data.playlists}));
	};

	render() {
        this.state.playlists = this.state.playlists.filter(function(playlist) {
            if (!_.isEmpty(playlist.image)) {
                console.log("NON-EMPTY PLAYLIST: " + JSON.stringify(playlist));
                return playlist;
            } else {
                console.log("EMPTY PLAYLIST: " + JSON.stringify(playlist));
            }
        });

        console.log(this.state.playlists);

		return (
			<div className={this.state.classnames}>
				{this.state.playlists.map(p => 
					<a href="/tracks" className="playlist-link" key={p.id}><div className="playlist-div">
						<div className="left-style">
                            <img src={p.image.url} alt=""/>
						</div>
						<p className="playlist-title">{p.name}</p>
					</div></a>
				)}
			</div>
		);
	}
}

export default Home;
