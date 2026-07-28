document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');
    const userPlaylistsDiv = document.getElementById('userPlaylists');
    const topPlaylistsDiv = document.getElementById('topPlaylists');

    loadTopPlaylists();

    if (!token) {
        userPlaylistsDiv.innerHTML = `
            <div class="text-center py-4">
                <p class="text-muted">Войдите в аккаунт или зарегистрируйтесь, чтобы создавать свои плейлисты</p>
            </div>`;
    } else {
        loadUserPlaylists(token);
    }

    async function loadUserPlaylists(token) {
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

            userPlaylistsDiv.innerHTML = renderPlaylists(playlists);

        } catch (err) {
            console.error(err);
            userPlaylistsDiv.innerHTML = '<p class="text-danger text-center py-4">Ошибка загрузки плейлистов</p>';
        }
    }

    async function loadTopPlaylists() {
        try {
            const response = await fetch('/users/playlist/top/', {
                headers: { 'Content-Type': 'application/json' }
            });
            
            if (!response.ok) throw new Error('Ошибка загрузки');
            
            const playlists = await response.json(); 
            
            if (!playlists || playlists.length === 0) {
                topPlaylistsDiv.innerHTML = '<p class="text-muted text-center py-4">Нет популярных плейлистов</p>';
                return;
            }

            topPlaylistsDiv.innerHTML = renderPlaylists(playlists);

        } catch (err) {
            console.error(err);
            topPlaylistsDiv.innerHTML = '<p class="text-muted text-center py-4">Не удалось загрузить</p>';
        }
    }

    function renderPlaylists(playlists) {
        return playlists.map(pl => `
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
    }

    document.addEventListener('click', (e)=>{
        const openButton = e.target.closest('.open-playlist-btn');

        if(openButton){
            const playlistId = openButton.dataset.id;
            window.location.href =`/playlist/${playlistId}/detail/`;
        }
    });
});