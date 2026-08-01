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

    document.getElementById('albumLikesCount').textContent = album.likes || 0;

    if (isOwner) {
        document.getElementById('likeAlbumBtn').style.display = 'none';

        document.getElementById('addTrackContainer').innerHTML = `
            <button class="btn btn-outline-secondary" id="addTrackBtn">
                <i class="fas fa-plus"></i> Добавить трек
            </button>
            <button class="btn btn-outline-secondary btn-sm" id="editAlbumBtn">
                <i class="fas fa-pen"></i>
            </button>
            <button class="btn btn-outline-danger btn-sm" id="deleteAlbumBtn">
                <i class="fas fa-trash"></i>
            </button>
        `;

        document.getElementById('addTrackBtn').addEventListener('click', () => {
            window.location.href = `/tracks/create/?album_id=${album.id}`;
        });

        document.getElementById('editAlbumBtn').addEventListener('click', () => {
            const newTitle = prompt('Новое название альбома:', album.title);
            if (!newTitle || newTitle === album.title) return;
            
            fetch(`/api/artists/album/${album.id}/update/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ title: newTitle })
            }).then(r => {
                if (r.ok) {
                    document.getElementById('albumTitle').textContent = newTitle;
                    album.title = newTitle;
                }
            });
        });

        document.getElementById('deleteAlbumBtn').addEventListener('click', async () => {
            if (!confirm('Удалить альбом?')) return;
            const res = await fetch(`/api/artists/album/${album.id}/delete/`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                alert('Альбом удалён');
                window.location.href = document.referrer || '/artist/my/';
            }
        });
    } else {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const userId = payload.user_id;
            const checkRes = await fetch(`/api/artists/album/like/${album.id}/check/?user_id=${userId}`);
            const checkData = await checkRes.json();
            if (checkData.is_liked) {
                document.getElementById('likeAlbumBtn').classList.add('liked');
            }
        } catch(e) {}
    }

    if (!isOwner) {
        document.getElementById('likeAlbumBtn').addEventListener('click', async () => {
            if (!token) return alert('Войдите чтобы лайкнуть');
            
            const res = await fetch(`/api/artists/album/like/${album.id}/`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await res.json();
            
            document.getElementById('albumLikesCount').textContent = data.likes;
            document.getElementById('likeAlbumBtn').classList.toggle('liked', data.status === 'liked');
        });
    }

    // Играть все
    document.getElementById('playAllBtn').addEventListener('click', () => {
        if (album.tracks?.length) {
            const trackIds = album.tracks.map(t => t.id).join(',');
            window.location.href = `/player/?track_id=${album.tracks[0].id}&playlist=${trackIds}`;
        }
    });

    document.getElementById('shareAlbumBtn')?.addEventListener('click', () => {
        navigator.clipboard.writeText(window.location.href).then(() => alert('Ссылка скопирована'));
    });

    document.addEventListener('click', (e) => {
        const row = e.target.closest('.track-row');
        if (row?.dataset.trackId) {
            window.location.href = `/track/card/${row.dataset.trackId}/`;
        }
    });
}