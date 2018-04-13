const callback_uri = 'http://localhost:8080/callback';

function saveAccessToken() {

    var req = new XMLHttpRequest();
    let url = '/login';

    var xhr = createCORSRequest('GET', url);
    if (!xhr) {
        throw new Error('CORS not supported');
    }

    xhr.onload = function() {
        if (xhr.status == 200) {
            console.log("SUCCESS: " + xhr.responseText);
        } else {
            console.log("FAIL: " + xhr.responseText);
        }
    }

    xhr.onerror = function() {
        console.log("ERROR: " + JSON.stringify(xhr));
    }

    xhr.send()

    /*
    req.open('GET', url);
    req.send();

    req.onreadystatechange = function() {
        if (req.status == 200) {
            console.log("SUCCESS: " + req.responseText)
        } else {
            console.log("FAIL: " + req.responseText);
        }
    }
    */
};

function createCORSRequest(method, url) {
    var xhr = new XMLHttpRequest();

    if ("withCredentials" in xhr) {
        // Check if the XMLHttpRequest object has a "withCredentials" property.
        // "withCredentials" only exists on XMLHTTPRequest2 objects.
        xhr.open(method, url, true);
    } else if (typeof XDomainRequest != "undefined") {
        // Otherwise, check if XDomainRequest.
        // XDomainRequest only exists in IE, and is IE's way of making CORS requests.
        xhr = new XDomainRequest();
        xhr.open(method, url);
    } else {
        // Otherwise, CORS is not supported by the browser.
        xhr = null;
    }

    return xhr;
}

