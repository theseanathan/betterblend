const callback_uri = 'http://localhost:8080/callback.html';
const req = new XMLHttpRequest();

function promptCallback() {
    var url = '/client_info';
    var auth_url = 'https://accounts.spotify.com/authorize?';

    req.open('GET', url);
    req.send();

    req.onreadystatechange = function() {
        if (req.status == 200) {
            var client_info = JSON.parse(req.responseText);
            var scope = 'user-read-private user-read-email';

            var auth_dict = {
                response_type: 'code',
                client_id: client_info.client_id,
                scope: scope,
                redirect_uri: callback_uri
            };

            var esc = encodeURIComponent;
            var query = Object.keys(auth_dict)
                .map(k => esc(k) + '=' + esc(auth_dict[k]))
                .join('&');

            var redirect_url = auth_url + query;
            console.log('Redirecting to: ' + redirect_url);

            window.location.replace(redirect_url);
        } else {
            console.log("Get client_info - Fail\n" + req.responseText);
        }
    }
};

function saveAccessToken() {
    var query = window.location.search.substring(1);

    var url = '/access_token?' + query;

    req.open('GET', url);
    req.send();

    req.onreadystatechange = function() {
        if (req.status == 200) {
            tokens = JSON.parse(req.responseText);
            localStorage.setItem('access_token', tokens.access_token);
            localStorage.setItem('refresh_token', tokens.refresh_token);
            localStorage.setItem('expires_in', tokens.expires_in);

            window.location.replace('/playlists')
        } else {
            console.log('FAIL: ' + req.responseText)
        }
    }
}
