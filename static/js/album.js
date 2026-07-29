document.addEventListener('DOMContentLoaded', async () => {
    const albumId = ALBUM_ID;
    const token = localStorage.getItem('access_token');
    
    if (!albumId) {
        document.body.innerHTML = '<p class="text-center text-danger py-5">Альбом не найден</p>';
        return;
    }

    try {
        const res = await fetch(`/api/artists/album/${albumId}/`);
        const album = await res.json();
        renderAlbum(album, token);
    } catch (err) {
        console.error(err);
        document.body.innerHTML = '<p class="text-center text-danger py-5">Ошибка загрузки</p>';
    }
});

async function renderAlbum(album, token) {
    document.getElementById('albumTitle').textContent = album.title;
    document.getElementById('albumArtist').textContent = album.artist_name || '';
    document.getElementById('albumInfo').textContent = 
        `${album.release_date || ''} • ${album.tracks?.length || 0} треков`;

    const coverContainer = document.getElementById('albumCoverContainer');
    if (album.cover) {
        coverContainer.innerHTML = `<img src="${album.cover}" class="album-cover" alt="">`;
    } else {
        coverContainer.innerHTML = getDefaultCoverSVG('150', '150', '8');
    }

    const tracksList = document.getElementById('albumTracksList');
    if (album.tracks && album.tracks.length > 0) {
        tracksList.innerHTML = album.tracks.map((track, i) => `
            <div class="track-row" data-track-id="${track.id}">
                <span class="track-number">${i + 1}</span>
                <div class="track-row-info">
                    <div class="track-row-title">${escapeHtml(track.title)}</div>
                    <div class="track-row-artist">${escapeHtml(track.genre_name || '')}</div>
                </div>
                <div class="track-row-meta">
                    <span class="track-stat">${formatPlays(track.plays_count || 0)}</span>
                    <span class="track-time">${formatDuration(track.duration)}</span>
                </div>
            </div>
        `).join('');
    } else {
        tracksList.innerHTML = '<p class="text-muted p-3">Нет треков</p>';
    }

    let isOwner = false;
    if (token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const userId = payload.user_id;

            const listRes = await fetch('/api/artists/list/');
            const artists = await listRes.json();
            const myArtist = artists.find(a => a.user === userId);

            if (myArtist && (myArtist.id === album.artist || myArtist.id === album.artist_id)) {
                isOwner = true;
            }
        } catch(e) {}
    }

    if (isOwner) {
        document.getElementById('addTrackContainer').innerHTML = `
            <button class="btn btn-outline-secondary" id="addTrackBtn">
                <i class="fas fa-plus"></i> Добавить трек
            </button>
        `;
        document.getElementById('addTrackBtn').addEventListener('click', () => {
            window.location.href = `/tracks/create/?album_id=${album.id}`;
        });
    }

    // Играть все
    document.getElementById('playAllBtn')?.addEventListener('click', () => {
        if (album.tracks?.length) {
            window.location.href = `/player/?track_id=${album.tracks[0].id}`;
        }
    });

    document.getElementById('shareAlbumBtn')?.addEventListener('click', () => {
        navigator.clipboard.writeText(window.location.href).then(() => alert('Ссылка скопирована'));
    });

    document.addEventListener('click', (e) => {
        const row = e.target.closest('.track-row');
        if (row?.dataset.trackId) {
            window.location.href = `/player/?track_id=${row.dataset.trackId}`;
        }
    });
}