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
        if (artist?.dataset.artistId) {
            window.location.href = `/artists/?artist_id=${artist.dataset.artistId}`;
            return;
        }
        const row = e.target.closest('.track-row');
        if (row?.dataset.trackId) {
            window.location.href = `/player/?track_id=${row.dataset.trackId}`;
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
        return tracks.map(track => `
            <div class="track-row" data-track-id="${track.id}">
                <img src="${track.cover || '/static/img/default-cover.png'}" 
                     class="track-row-cover" alt=""
                     onerror="this.style.display='none'">
                <div class="track-row-info">
                    <div class="track-row-title">${escapeHtml(track.title)}</div>
                    <div class="track-row-artist" data-artist-id="${track.artist?.id || ''}">
                        ${escapeHtml(track.artist?.name || 'Неизвестен')}
                    </div>
                </div>
                <div class="track-row-meta">
                    <span class="track-badge">${escapeHtml(track.genre?.name || '—')}</span>
                    <span class="track-stat">${formatPlays(track.plays_count || 0)}</span>
                    <span class="track-time">${formatDuration(track.duration || 0)}</span>
                </div>
            </div>
        `).join('');
    }

    // =================================
    //  УТИЛИТЫ

    function formatDuration(seconds) {
        if (!seconds || isNaN(seconds)) return '0:00';
        const m = Math.floor(seconds / 60);
        const s = Math.floor(seconds % 60);
        return `${m}:${s.toString().padStart(2, '0')}`;
    }

    function formatPlays(count) {
        if (count >= 1000000) return (count / 1000000).toFixed(1) + 'M';
        if (count >= 1000) return (count / 1000).toFixed(1) + 'K';
        return String(count);
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});