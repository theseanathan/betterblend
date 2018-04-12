//app.js 
const app = express();

const bodyParser = require('body-parser');
const client_info = require('./client_info.json');
const express = require('express');
const querystring = require('querystring');

app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static('public'));

app.set('view engine', 'hbs');


app.get('/', (req, res) => {
    var callback_uri = 'http://localhost:8080/callback';
    var scope = 'user-read-private user-read-email';
    var url = 'https://accounts.spotify.com/authorize?';

    var auth_dict = {
        response_type: 'code',
        client_id: client_info.client_id,
        scope: scope,
        redirect_uri: callback_uri
    };

    res.redirect(url + querystring.stringify(auth_dict));
});

app.get('/callback', (req, res) => {
    var code = req.query.code;
});

app.get('/playlists', (req, res) => {
	res.render('playlists');
});

app.listen(8080);
