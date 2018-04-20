document.addEventListener('DOMContentLoaded', main);

function main() {
	getTracks();
}

function getTracks() {
	let req = new XMLHttpRequest();
	let urls = 'http://localhost:5000/get_tracks?access_token=' + localStorage.getItem('access_token');
	req.open('GET', urls);
	req.addEventListener('load', function(evt) {
		let t = document.querySelector('#tracks')
		if(req.status >= 200 && req.status < 300) {
			const tracks = JSON.parse(req.responseText);
            console.log(tracks);
			for(const p of tracks.tracks) {
				appendToDiv(t, p);
			}
		}
	});
	req.send();
}

function appendToDiv(t, p) {
    const tr = document.createElement('div');
    tr.href = '/tracks';
    tr.classList.add('playlist-item');
    tr.appendChild(document.createTextNode(p.name));
    t.appendChild(tr);
}