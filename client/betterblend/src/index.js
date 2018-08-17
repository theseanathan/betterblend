import React from 'react';
import ReactDOM from 'react-dom';
import { 
	BrowserRouter as Router,
	Switch,
	Route
	//Link 
} from 'react-router-dom';
import Home from './Home.js';
import Login from './components/Login.js';
import Track from './components/Track.js';
import './index.css';
import './css/skeleton.css';
import './css/normalize.css';
import registerServiceWorker from './registerServiceWorker';

const Header = () => (
	<header>
		<h3>BetterBlend</h3>
		<h5><i>King of all blenders</i></h5>
	</header>
)

const Main = () => (
	<main>
		<Switch>
			<Route exact path='/' component={Login}/>
			<Route path='/playlists' component={Home}/>
			<Route name='/playlists/:idNum' component={Track}/>
		</Switch>
	</main>
)

const App = () => (
	<div className="container">
		<Header/>
		<Main/>
	</div>
)

ReactDOM.render(
	(<Router>
		<App/>
	</Router>
	),document.getElementById('root')
);
registerServiceWorker();
