//app.js 
const express = require('express');
const app = express();
const bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({ extended: false }));

app.use(express.static('public'));

app.set('view engine', 'hbs');

app.get('/', (req, res) => {
	res.render('index');
});

app.get('/playlists', (req, res) => {
	res.render('playlists');
});

app.get('/playlist-tracks', (req, res) => {
	res.render('playlist_tracks');
});

app.listen(8080);