document.addEventListener('DOMContentLoaded', main);

function main() {
	getTracks();
}

function getTracks() {
	let req = new XMLHttpRequest();
	let urls = 'http://localhost:3000/response';
	req.open('GET', urls);
	req.addEventListener('load', function(evt) {
		let t = document.querySelector('#tracks-list')
		if(req.status >= 200 && req.status < 300) {
			const tracks = JSON.parse(req.responseText);
			for(const p of tracks.tracks) {
				appendTable(t, p);
			}
		}
	});
	req.send();
}

function appendTable(t, p) {
	const tr = document.createElement('tr');
    const n = document.createElement('td');
    n.appendChild(document.createTextNode(p.name));
    const c = document.createElement('td');
    c.appendChild(document.createTextNode(p.artist));
    const i = document.createElement('td');
    const iTag = document.createElement('i');
    const iTag2 = document.createElement('i');
    iTag.classList.add('fas');
    iTag.classList.add('fa-thumbs-up');
    iTag.classList.add('fa-lg');
    iTag.classList.add('vote');
    iTag2.classList.add('fas');
    iTag2.classList.add('fa-thumbs-down');
    iTag2.classList.add('fa-lg');
    iTag2.classList.add('vote');
    i.appendChild(iTag);
    i.appendChild(iTag2);
    tr.appendChild(n);
    tr.appendChild(c);
    tr.appendChild(i);
    t.appendChild(tr);
}