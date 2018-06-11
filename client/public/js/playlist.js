document.addEventListener('DOMContentLoaded', main);

function main() {
	getPlaylists();
}

function getPlaylists() {
	let req = new XMLHttpRequest();
    //let urls = 'http://localhost:3000/response';
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
	const card = document.createElement('div');
	card.classList.add('card');

	const cardImage = document.createElement('div');
	cardImage.classList.add('card-image');
	const figure = document.createElement('figure');
	figure.classList.add('image');
	figure.classList.add('is-square');
	const img = document.createElement('img');
	img.src = "https://bulma.io/images/placeholders/480x480.png"; //image here
	figure.appendChild(img);
	cardImage.appendChild(figure);
	card.appendChild(cardImage);

	const cardContent = document.createElement('div');
	cardContent.classList.add('card-content');
	const media = document.createElement('div');
	media.classList.add('media');
	const mediaContent = document.createElement('div');
	mediaContent.classList.add('media-content');
	const playlist = document.createElement('p');
	playlist.classList.add('title');
	playlist.classList.add('is-6');
	playlist.style.textAlign = 'center';
	const link = document.createElement('a');
	link.appendChild(document.createTextNode(p.name)); //playlist name here
	link.href = "/tracks";                             //href link here
	playlist.appendChild(link);
	mediaContent.appendChild(playlist);
	media.appendChild(mediaContent);
	cardContent.appendChild(media);
	card.appendChild(cardContent);

	t.appendChild(card);
}

/*
<div class="card">
	<div class="card-image">
		<figure class="image is-square">
			<img src="https://bulma.io/images/placeholders/480x480.png" alt="Placeholder image">
		</figure>
	</div>
	<div class="card-content">
		<div class="media">
			<div class="media-content">
				<p class="title is-6" style="text-align:center;"><a href="/tracks">Playlist</a></p>
			</div>
		</div>
	</div>
</div>
*/