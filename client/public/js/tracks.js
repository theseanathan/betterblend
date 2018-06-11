document.addEventListener('DOMContentLoaded', main);

function main() {
	getTracks();
}

function getTracks() {
	let req = new XMLHttpRequest();
	//let urls = 'http://localhost:3000/response';
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
	const box = document.createElement('div');
	box.classList.add('box');
	const media = document.createElement('div');
	media.classList.add('media');
	
	const mediaLeft = document.createElement('div');
	mediaLeft.classList.add('media-left');
	const figure = document.createElement('figure');
	figure.classList.add('image');
	figure.classList.add('is-64x64');
	const img = document.createElement('img');
	img.src = "https://bulma.io/images/placeholders/128x128.png"; //image here
	figure.appendChild(img);
	mediaLeft.appendChild(figure);
	media.appendChild(mediaLeft);

	const mediaContent = document.createElement('div');
	mediaContent.classList.add('media-content');
	const content = document.createElement('div');
	content.classList.add('content');
	const p1 = document.createElement('p');
	const p2 = document.createElement('p');
	p1.classList.add('names');
	p1.classList.add('song-name');
	p2.classList.add('names');
	p2.classList.add('artist-name');
	p1.appendChild(document.createTextNode(p.name));
	p2.appendChild(document.createTextNode(p.artist));
	content.appendChild(p1);
	content.appendChild(document.createElement('br'));
	content.appendChild(p2);
	mediaContent.appendChild(content);

	const nav = document.createElement('nav');
	nav.classList.add('level');
	nav.classList.add('is-mobile');
	const left = document.createElement('div');
	left.classList.add('level-left');
	const a1 = document.createElement('a');
	a1.classList.add('level-item');
	const span1 = document.createElement('span');
	span1.classList.add('icon');
	span1.classList.add('is-small');
	const i1 = document.createElement('i');
	i1.classList.add('fas');
	i1.classList.add('fa-chevron-circle-up');
	span1.appendChild(i1);
	a1.appendChild(span1);
	const a2 = document.createElement('a');
	a2.classList.add('level-item');
	const span2 = document.createElement('span');
	span2.classList.add('icon');
	span2.classList.add('is-small');
	const i2 = document.createElement('i');
	i2.classList.add('fas');
	i2.classList.add('fa-chevron-circle-up');
	span2.appendChild(i2);
	a2.appendChild(span2);
	left.appendChild(a1);
	left.appendChild(a2);
	const right = document.createElement('div');
	right.classList.add('level-right');
	right.appendChild(document.createTextNode(p.vote_count));
	nav.appendChild(left);
	nav.appendChild(right);

	mediaContent.appendChild(nav);
	media.appendChild(mediaContent);
	box.appendChild(media);
	t.appendChild(box);
}

/*<div class="box">
	<div class="media">
		<div class="media-left">
			<figure class="image is-64x64">
				<img src="https://bulma.io/images/placeholders/128x128.png">
			</figure>
		</div>
		<div class="media-content">
			<div class="content">
				<p class="names"><strong>Song NameSong NameSong NameSong NameSong NameSong NameSong Name</strong></p><br>
				<p class="names"><small>ArtistArtistArtistArtistArtistArtistArtistArtist</small></p>
			</div>
			<nav class="level is-mobile">
				<div class="level-left">
					<a class="level-item" aria-label="up">
						<span class="icon is-small">
							<i class="fas fa-chevron-circle-up"></i>
						</span>
					</a>
					<a class="level-item" aria-label="down">
						<span class="icon is-small">
							<i class="fas fa-chevron-circle-down"></i>
						</span>
					</a>
				</div>
				<div class="level-right">69</div>
			</nav>
		</div>
	</div>
</div>*/