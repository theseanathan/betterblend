document.addEventListener('DOMContentLoaded', main);

function main() {
	getPlaylists();
}

function getPlaylists() {
	let req = new XMLHttpRequest();
    // let urls = 'http://localhost:3000/response';
	let urls = 'http://localhost:5000/get_playlists?access_token=' + localStorage.getItem('access_token');
	req.open('GET', urls);
	//req.onreadystatechange = function() {
	req.addEventListener('load', function(evt) {
		let t = document.querySelector('#playlist');
		if(req.status >= 200 && req.status < 300) {
            const lists = JSON.parse(req.responseText);
            console.log(lists);
			for(const p of lists.playlists) {
				appendToDiv(t, p);
			}
		}
	})
	req.send();
}

function appendToDiv(t, p) {
	const tr = document.createElement('a');
	tr.href = '/tracks';
	tr.classList.add('playlist-item');
	//tr.classList.add('shadow');
	tr.classList.add('scaling');
    //const n = document.createElement('a');
    tr.appendChild(document.createTextNode(p.name));
    //tr.appendChild(n);
    t.appendChild(tr);
}
