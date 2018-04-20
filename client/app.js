// app.js 
const atob = require('atob')
const bodyParser = require('body-parser');
const btoa = require('btoa')
const client_info = require('./client_info.json');
const express = require('express');
const querystring = require('querystring');
const request = require('request')

const app = express();
const callback_uri = 'http://localhost:8080/callback.html';

app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static('public'));

app.set('view engine', 'hbs');

app.get('/', (req, res) => {
    res.render('login')    
});

app.get('/login', (req, res) => {
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

app.get('/client_info', (req, res) => {
    res.send(client_info);
});

app.get('/access_token', (req, res) => {
    var code = req.query.code;
    var url = 'https://accounts.spotify.com/api/token';

    var token_dict = {
        grant_type: "authorization_code",
        code: code,
        redirect_uri: callback_uri
    };

    var client_info_encrypted_btoa = btoa(client_info.client_id + ':' + client_info.client_secret)
    var headers = { 'Authorization': 'Basic ' + client_info_encrypted_btoa };

    var auth_dict = {
        url: url,
        form: token_dict,
        headers: headers,
        json: true,
    };

    request.post(auth_dict, function(error, response, body) {
        if (!error && response.statusCode == 200) {
            console.log('access_token: ' + body.access_token);
            console.log('refresh_token: ' + body.refresh_token);

            res.send({
                'access_token': body.access_token, 
                'refresh_token': body.refresh_token,
                'expires_in': body.expires_in
            });
            // res.end(body.access_token);
        } else {
            console.log("RESPONSE: " + JSON.stringify(response))
            console.log("BODY: " + JSON.stringify(body))
        }
    });
});

app.get('/playlists', (req, res) => {
	res.render('playlists');
});

app.get('/tracks', (req, res) => {
    console.log(req.body);
    res.render('playlist_tracks');
});

app.listen(8080);
