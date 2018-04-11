function main() {
	let x = document.querySelector("#playlists");

}

function appendTable(t, p) {
	const tr = document.createElement('tr');
    const n = document.createElement('td');
    n.appendChild(document.createTextNode(p.name));
    const c = document.createElement('td');
    c.appendChild(document.createTextNode(p.cuisine));
    const l = document.createElement('td');
    l.appendChild(document.createTextNode(p.location));
    tr.appendChild(n);
    tr.appendChild(c);
    tr.appendChild(l);
    t.appendChild(tr);
}

document.addEventListener('DOMContentLoaded', main);