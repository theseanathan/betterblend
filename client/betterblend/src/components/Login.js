import React, { Component } from 'react';
import '../index.css';

class Login extends Component {

	constructor() {
		super();
		this.state = {
			classnames: ''
		}
	}

	render() {
		return (
			<div className={this.state.classnames}>
				<a className="links" href="/playlists">Login</a>
			</div>
		);
	}
}

export default Login;