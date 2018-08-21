import React, { Component } from 'react';
import '../css/playlist.css';
import axios from 'axios';

class Track_Form extends Component {

	constructor() {
		super();
		this.state = {
			classnames: 'song-data'
		}
		this.upVote = this.upVote.bind(this);
		this.downVote = this.downVote.bind(this);
	}

	upVote = (e) => {
		e.preventDefault();
		//axios.put('/vote_track?id='+this.props.trackInfo.id+'?vote=1')
		//.then().catch(err => console.log(err.response.data));
		axios.put('/vote_track', {
            'id': this.props.trackInfo.id,
            'vote': 1
		}).then().catch(err => console.log(err.response.data));
	};

	downVote = (e) => {
		e.preventDefault();
		axios.put('/vote_track', {
            id: this.props.trackInfo.id,
            vote: -1
		}).then().catch(err => console.log(err.response.data));
	};

	render() {
		return (
			<div className={this.state.classnames}>
				<div className="vote-buttons" onClick={this.upVote}><a><i className="fa fa-caret-up fa-lg"></i></a></div>
				<div className="vote-buttons" onClick={this.downVote}><a><i className="fa fa-caret-down fa-lg"></i></a></div>
				<div><p className="count-num">{this.props.trackInfo.vote_count}</p></div>
			</div>
		);
	}
}

export default Track_Form;