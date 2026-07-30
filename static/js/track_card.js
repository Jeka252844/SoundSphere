document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');
    const trackId = TRACK_ID;

    if (!trackId) {
        showMessageModal('Трек не найден', '', 'Назад', 'back');
        return;
    }

    try {
        const res = await fetch(`/api/tracks/${trackId}/`);
        const track = await res.json();
        renderTrackCard(track, token);
    } catch (err) {
        showMessageModal('Ошибка загрузки', '', 'Назад', 'back');
    }

    document.getElementById('closePlaylistModal')?.addEventListener('click', closePlaylistModal);
    document.getElementById('cancelPlaylist')?.addEventListener('click', closePlaylistModal);
    document.getElementById('playlistModal')?.addEventListener('click', (e) => {
        if (e.target === e.currentTarget) closePlaylistModal();
    });
});

async function renderTrackCard(track, token) {
    document.querySelector('.track-detail-title').textContent = track.title;
    document.querySelector('.track-detail-artist').textContent = track.artist_name || 'Неизвестен';

    // Обложка
    const coverContainer = document.querySelector('.default-avatar-svg');
    if (track.cover) {
        coverContainer.innerHTML = `<img src="${track.cover}" style="width:100%;height:100%;object-fit:cover;position:absolute;top:0;left:0;">`;
    } else {
        coverContainer.innerHTML = getDefaultCoverSVG('100%', '100%', '0');
    }

    let isOwner = false;
    if (token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const userId = payload.user_id;

            const listRes = await fetch('/api/artists/list/');
            const artists = await listRes.json();
            const myArtist = artists.find(a => a.user === userId);

            if (myArtist && track.artist_id === myArtist.id) {
                isOwner = true;
            }
        } catch(e) {}
    }

    // Кнопка слушать
    document.querySelector('.btn-listen-main').addEventListener('click', () => {
        window.location.href = `/player/?track_id=${track.id}`;
    });

    if (isOwner) {
        const likeBtn = document.querySelector('.action-icon-btn[title="Лайк"]');
        if (likeBtn) likeBtn.style.display = 'none';
    }

    // Кнопка удалить
    if (isOwner) {
        const actionsRow = document.querySelector('.track-actions-row');
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'action-icon-btn';
        deleteBtn.title = 'Удалить';
        deleteBtn.innerHTML = `
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
            <span>Удалить</span>
        `;
        deleteBtn.addEventListener('click', async () => {
            if (!confirm('Удалить трек?')) return;
            const res = await fetch(`/api/tracks/${track.id}/delete/`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                alert('Трек удалён');
                history.back();
            }
        });
        actionsRow.appendChild(deleteBtn);
    }

    // добавить в плейлист
    document.querySelector('.action-icon-btn[title="В плейлист"]').addEventListener('click', () => {
        openPlaylistModal(track.id);
    });

    // Поделиться
    document.querySelector('.action-icon-btn[title="Поделиться"]').addEventListener('click', () => {
        navigator.clipboard.writeText(window.location.href).then(() => alert('Ссылка скопирована'));
    });

    // Жалоба
    document.querySelector('.report-btn').addEventListener('click', () => {
        showReportModal('track', track.id, track.title);
    });
}

async function openPlaylistModal(trackId) {
    const token = localStorage.getItem('access_token');
    if (!token) {
        showMessageModal('Вы не авторизованы', 'Войдите чтобы добавлять в плейлисты', 'Войти', '/login/');
        return;
    }

    const modal = document.getElementById('playlistModal');
    const body = document.getElementById('playlistListBody');
    modal.style.display = 'flex';
    body.innerHTML = '<p class="text-muted text-center">Загрузка...</p>';

    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const userId = payload.user_id;
        const userRes = await fetch(`/users/${userId}/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const user = await userRes.json();
        const playlists = user.playlists || [];

        if (playlists.length === 0) {
            body.innerHTML = `
                <p class="text-muted text-center py-3">У вас нет плейлистов</p>
                <div class="text-center pb-3">
                    <button class="btn btn-outline-secondary btn-sm" id="createPlaylistFromModal">
                        <i class="fas fa-plus"></i> Создать плейлист
                    </button>
                </div>
            `;

            document.getElementById('createPlaylistFromModal').addEventListener('click', () => {
                const title = prompt('Название плейлиста:');
                if (!title) return;
                fetch('/users/playlist/create/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ title })
                }).then(r => r.json()).then(() => {
                    openPlaylistModal(trackId);
                });
            });
        } else {
            body.innerHTML = playlists.map(pl => `
                <div class="playlist-option" data-id="${pl.id}" style="
                    display:flex;align-items:center;gap:12px;padding:10px 12px;cursor:pointer;
                    border-radius:8px;transition:background 0.2s;
                ">
                    <div>
                        <div style="color:#fff;">${escapeHtml(pl.title)}</div>
                        <div style="font-size:0.75rem;color:#999;">${pl.tracks_count || 0} треков</div>
                    </div>
                </div>
            `).join('');

            // Клик по плейлисту
            body.querySelectorAll('.playlist-option').forEach(opt => {
                opt.addEventListener('click', async () => {
                    const playlistId = opt.dataset.id;
                    const res = await fetch(`/users/playlist/${playlistId}/add/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify({ track_id: trackId })
                    });
                    const data = await res.json();
                    
                    if (res.ok) {
                        alert('Добавлено!');
                        closePlaylistModal();
                    } else {
                        alert(data.error || 'Ошибка');
                        closePlaylistModal();
                    }
                });
            });
        }
    } catch (err) {
        showMessageModal('Ошибка загрузки', '', 'Назад', 'back');
    }

    body.querySelectorAll('.playlist-option').forEach(opt => {
        opt.addEventListener('mouseenter', () => opt.style.background = 'rgba(255,255,255,0.04)');
        opt.addEventListener('mouseleave', () => opt.style.background = 'transparent');
    });
}

function closePlaylistModal() {
    document.getElementById('playlistModal').style.display = 'none';
}