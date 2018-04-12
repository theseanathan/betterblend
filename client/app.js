//app.js 
const atob = require('atob')
const bodyParser = require('body-parser');
const btoa = require('btoa')
const client_info = require('./client_info.json');
const express = require('express');
const querystring = require('querystring');
const request = require('request')

const app = express();
const callback_uri = 'http://localhost:8080/callback';

app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static('public'));

app.set('view engine', 'hbs');


app.get('/', (req, res) => {
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
            // TODO: Save tokens to HTML5 Web Storage, route to HOME page.
        } else {
            console.log("RESPONSE: " + JSON.stringify(response))
            console.log("BODY: " + JSON.stringify(body))
        }
    });
});

app.get('/playlists', (req, res) => {
	res.render('playlists');
});

app.listen(8080);
