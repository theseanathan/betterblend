import React, { Component } from 'react';
import '../css/playlist.css';
import axios from 'axios';

class Track_Form extends Component {

	constructor(props) {
		super(props);
		this.state = {
			classnames: 'song-data',
			counts: props.trackInfo.vote_count
		}
		this.upVote = this.upVote.bind(this);
		this.downVote = this.downVote.bind(this);
	}

	upVote = (e) => {
		e.preventDefault();
		axios.put('/vote_track', {
            'id': this.props.trackInfo.id,
            'vote': 1
		}).then(this.update()).catch(err => console.log(err.response));
	};

	downVote = (e) => {
		e.preventDefault();
		axios.put('/vote_track', {
            id: this.props.trackInfo.id,
            vote: -1
		}).then(this.update()).catch(err => console.log(err.response.data));
	};

	update = (props) => {
		const trackUrl = '/get_playlist?id='+ this.props.trackInfo.playlist_id;
		axios.get(trackUrl)
		.then(data => {
			let ind = this.props.index;
			this.setState({counts: data.data.tracks[ind].vote_count});
		});
	};

	render() {
		//console.log(this.props);
		return (
			<div className={this.state.classnames}>
				<div className="vote-buttons" onClick={this.upVote}><a><i className="fa fa-caret-up fa-lg"></i></a></div>
				<div className="vote-buttons" onClick={this.downVote}><a><i className="fa fa-caret-down fa-lg"></i></a></div>
				<div><p className="count-num">{this.state.counts}</p></div>
			</div>
		);
	}
}

export default Track_Form;