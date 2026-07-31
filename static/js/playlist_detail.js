document.addEventListener('DOMContentLoaded', async () => {
    const playlistId = PLAYLIST_ID;
    const token = localStorage.getItem('access_token');
    let playlistData = null;

    if (!playlistId) {
        showMessageModal('Плейлист не найден', '', 'Назад', 'back');
        return;
    }

    try {
        const res = await fetch(`/users/playlist/${playlistId}/`, {
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        playlistData = await res.json();
        renderPlaylist(playlistData, token);
    } catch (err) {
        showMessageModal('Ошибка загрузки', '', 'Назад', 'back');
    }
});

async function renderPlaylist(data, token) {
    const playlistId = PLAYLIST_ID;
    
    document.getElementById('playlistName').textContent = data.title;
    document.getElementById('playlistAuthor').textContent = data.user || 'Неизвестен';
    document.getElementById('playlistStats').textContent = 
        `${data.tracks_count || 0} треков • ${data.likes || 0} ❤️`;
    document.getElementById('likesCount').textContent = data.likes || 0;

    let isOwner = false;
    if (token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const userId = payload.user_id;
            const userRes = await fetch(`/users/${userId}/`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const user = await userRes.json();
            if (user.username === data.user || user.id === data.user_id) {
                isOwner = true;
            }
        } catch(e) {}
    }

    // Обложка
    const coverDiv = document.getElementById('playlistCover');
    if (data.cover) {
        coverDiv.innerHTML = `<img src="${data.cover}" alt="">`;
    } else {
        coverDiv.innerHTML = getDefaultCoverSVG('140', '140', '8');
        const svg = coverDiv.querySelector('svg');
        if (svg) { svg.style.width = '100%'; svg.style.height = '100%'; }
    }

    // Треки
    const tracksDiv = document.getElementById('playlistTracks');
    if (data.tracks && data.tracks.length > 0) {
        tracksDiv.innerHTML = data.tracks.map(track => `
            <div class="track-row" data-track-id="${track.id}">
                ${track.cover ? `<img src="${track.cover}" class="track-row-cover" alt="">` : getDefaultCoverSVG('44','44','6')}
                <div class="track-row-info">
                    <div class="track-row-title">${escapeHtml(track.title)}</div>
                    <div class="track-row-artist">${escapeHtml(track.artist_name || 'Неизвестен')}</div>
                </div>
                <div class="track-row-meta">
                    <span class="track-time">${formatDuration(track.duration)}</span>
                </div>
            </div>
        `).join('');
    } else {
        tracksDiv.innerHTML = '<p class="text-muted text-center py-4">Нет треков</p>';
    }

    const actionsDiv = document.querySelector('.playlist-action-btns');
    
    if (isOwner) {
        actionsDiv.innerHTML = `
            <button class="action-btn" id="btnShare" title="Поделиться">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path></svg>
            </button>
            <button class="action-btn" id="btnDelete" title="Удалить" style="color:#ef4444;border-color:#ef4444;">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
            </button>
        `;

        document.getElementById('btnDelete').addEventListener('click', async () => {
            if (!confirm('Удалить плейлист?')) return;
            const res = await fetch(`/users/playlist/${playlistId}/delete/`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                alert('Плейлист удалён');
                window.location.href = '/playlist/my/'
            }
        });
    } else {
        actionsDiv.innerHTML = `
            <button class="action-btn" id="btnLike" title="Лайк">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
                <span id="likesCount">${data.likes || 0}</span>
            </button>
            <button class="action-btn" id="btnShare" title="Поделиться">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path></svg>
            </button>
            <button class="action-btn report-btn" id="btnReport" title="Пожаловаться">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9"></path></svg>
            </button>
        `;

        document.getElementById('btnLike').addEventListener('click', async () => {
            if (!token) return alert('Войдите чтобы лайкнуть');
            const res = await fetch(`/users/playlist/${playlistId}/like/`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const result = await res.json();
            document.getElementById('likesCount').textContent = result.likes;
            document.getElementById('btnLike').classList.toggle('liked', result.status === 'liked');
        });

        document.getElementById('btnReport').addEventListener('click', () => {
            showReportModal('playlist', playlistId, data.title);
        });
    }

    // Играть все
    document.getElementById('btnPlayAll').addEventListener('click', () => {
        if (data.tracks?.length) {
            window.location.href = `/player/?track_id=${data.tracks[0].id}`;
        }
    });

    // Поделиться
    document.getElementById('btnShare').addEventListener('click', () => {
        navigator.clipboard.writeText(window.location.href).then(() => alert('Ссылка скопирована'));
    });

    document.addEventListener('click', (e) => {
        const row = e.target.closest('.track-row');
        if (row?.dataset.trackId) {
            window.location.href = `/track/card/${row.dataset.trackId}/`;
        }
    });
}