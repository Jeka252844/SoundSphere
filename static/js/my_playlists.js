document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');
    const userPlaylistsDiv = document.getElementById('userPlaylists');

    if (!token) {
        userPlaylistsDiv.innerHTML = `
            <div class="text-center py-4">
                <p class="text-muted">Войдите в аккаунт или зарегистрируйтесь, чтобы создавать свои плейлисты</p>
            </div>`;
        return;
    }

    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const userId = payload.user_id;

        const response = await fetch(`/users/${userId}/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error('Ошибка загрузки');

        const user = await response.json();
        const playlists = user.playlists;

        if (!playlists || playlists.length === 0) {
            userPlaylistsDiv.innerHTML = '<p class="text-muted text-center py-4">У вас пока нет плейлистов</p>';
            return;
        }

        userPlaylistsDiv.innerHTML = playlists.map(pl => `
            <div class="playlist-card">
                <div class="playlist-cover">
                    ${pl.cover 
                        ? `<img src="${pl.cover}" alt="">`
                        : getDefaultCoverSVG('100%', '100%', '0')}
                </div>
                <div class="playlist-info">
                    <h3 class="playlist-title">${escapeHtml(pl.title)}</h3>
                    <p class="playlist-likes">${pl.tracks_count || 0} треков</p>
                    <div class="playlist-actions">
                        <button class="btn btn-primary btn-small open-playlist-btn" data-id="${pl.id}">
                            Открыть
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

    } catch (err) {
        showMessageModal('Ошибка загрузки', 'Не удалось загрузить плейлисты', 'Назад', 'back');
    }

    document.addEventListener('click', (e) => {
        const openButton = e.target.closest('.open-playlist-btn');
        if (openButton) {
            window.location.href = `/playlist/${openButton.dataset.id}/detail/`;
        }
    });
});