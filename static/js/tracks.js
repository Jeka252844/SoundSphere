document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const clearSearch = document.getElementById('clearSearch');
    const searchWrapper = document.getElementById('searchWrapper');
    const searchDropdown = document.getElementById('searchDropdown');
    const searchResults = document.getElementById('searchResults');
    const defaultContent = document.getElementById('defaultContent');
    const topTrackList = defaultContent.querySelector('.track-list');
    const searchResultsList = document.getElementById('searchResultsList');

    loadTopTracks();

    searchInput.addEventListener('focus', () => {
        if (!searchInput.value.trim()) {
            searchDropdown.classList.add('active');
        }
    });

    document.addEventListener('click', (e) => {
        if (!searchWrapper.contains(e.target)) {
            searchDropdown.classList.remove('active');
        }
    });

    searchDropdown.addEventListener('click', (e) => {
        const item = e.target.closest('.dropdown-item');
        if (item) {
            const query = item.textContent.trim();
            searchInput.value = query;
            searchDropdown.classList.remove('active');
            clearSearch.style.display = 'flex';
            searchTracks(query);
        }
    });

    let searchTimeout;
    searchInput.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        const query = searchInput.value.trim();
        
        clearSearch.style.display = query ? 'flex' : 'none';
        
        if (!query) {
            searchResults.style.display = 'none';
            defaultContent.style.display = 'block';
            searchDropdown.classList.remove('active');  
            return;
        }
        
        searchDropdown.classList.remove('active');  
        searchTimeout = setTimeout(() => searchTracks(query), 300);
    });

    clearSearch.addEventListener('click', () => {
        searchInput.value = '';
        clearSearch.style.display = 'none';
        searchResults.style.display = 'none';
        defaultContent.style.display = 'block';
        searchInput.focus();
    });

    document.addEventListener('click', (e) => {
        const artist = e.target.closest('.track-row-artist');
        if (artist) {
            e.stopPropagation();
            const artistId = artist.getAttribute('data-artist-id');
            window.location.href = `/artists/?artist_id=${artistId}`;
            return;
        }
    
        const row = e.target.closest('.track-row');
        if (row?.dataset.trackId) {
            window.location.href = `/track/card/${row.dataset.trackId}/`;
        }
    });

    // =====================================
    //   ФУНКЦИИ 

    async function loadTopTracks() {
        try {
            const res = await fetch('/api/tracks/top/');
            const data = await res.json();
            topTrackList.innerHTML = renderTracks(data);
        } catch (err) {
            topTrackList.innerHTML = '<p class="text-muted p-3">Ошибка загрузки</p>';
        }
    }

    async function searchTracks(query) {
        try {
            const res = await fetch(`/api/tracks/search/?query=${encodeURIComponent(query)}`);
            const data = await res.json();
            defaultContent.style.display = 'none';
            searchResults.style.display = 'block';
            searchResultsList.innerHTML = data.length 
                ? renderTracks(data) 
                : '<p class="text-muted p-3">Ничего не найдено</p>';
        } catch (err) {
            console.error(err);
        }
    }

    function renderTracks(tracks) {
        if (!tracks || tracks.length === 0) {
            return '<p class="text-muted p-3">Треки не найдены</p>';
        }
        
        return tracks.map(track => {
            const artistId = track.artist_id || track.artist?.id || '';
            const coverUrl = track.cover || null;
            
            console.log('Рисую трек:', track.title, 'cover:', coverUrl);
            
            return `
                <div class="track-row" data-track-id="${track.id}">
                    ${coverUrl 
                        ? `<img src="${coverUrl}" class="track-row-cover" alt="">`
                        : getDefaultCoverSVG('80', '80', '100')}
                    <div class="track-row-info">
                        <div class="track-row-title">${escapeHtml(track.title)}</div>
                        <div class="track-row-artist" data-artist-id="${artistId}">
                            ${escapeHtml(track.artist_name || track.artist?.name || 'Неизвестен')}
                        </div>
                    </div>
                    <div class="track-row-meta">
                        <span class="track-badge">${escapeHtml(track.genre_name || track.genre?.name || '—')}</span>
                        <span class="track-stat">${formatPlays(track.plays_count || 0)}</span>
                        <span class="track-time">${formatDuration(track.duration || 0)}</span>
                    </div>
                </div>
            `;
        }).join('');
    }
});