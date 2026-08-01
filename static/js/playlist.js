document.addEventListener('DOMContentLoaded', async () => {
    const topPlaylistsDiv = document.getElementById('topPlaylists');

    loadTopPlaylists();

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

        }  catch (err) {
            showMessageModal('Ошибка загрузки', 'Не удалось загрузить плейлисты', 'Назад', 'back');
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
                    <p class="playlist-likes">
                        ❤️ ${pl.likes || 0} • ${pl.tracks_count || 0} треков
                    </p>
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