document.addEventListener('DOMContentLoaded', main);

function main() {
	getPlaylists();
}

function getPlaylists() {
	let req = new XMLHttpRequest();
    // let urls = 'http://localhost:3000/response';
	let urls = 'http://localhost:5000/get_playlists?access_token=' + localStorage.getItem('access_token');
	req.open('GET', urls);
	req.onreadystatechange = function() {
		let t = document.querySelector('#playlist-list')
		if(req.status >= 200 && req.status < 300) {
            const lists = JSON.parse(req.responseText);
			for(const p of lists.playlists) {
				appendTable(t, p);
			}
		}
	};
	req.send();
}

function appendTable(t, p) {
	const tr = document.createElement('tr');
    const n = document.createElement('td');
    n.appendChild(document.createTextNode(p.name));
    const c = document.createElement('td');
    c.appendChild(document.createTextNode(p.id));
    const l = document.createElement('td');
    l.appendChild(document.createTextNode(p.href));
    tr.appendChild(n);
    tr.appendChild(c);
    tr.appendChild(l);
    t.appendChild(tr);
}
