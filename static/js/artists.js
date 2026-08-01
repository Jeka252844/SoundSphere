document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const clearSearch = document.getElementById('clearSearch');
    const searchResults = document.getElementById('searchResults');
    const defaultContent = document.getElementById('defaultContent');
    const topList = document.getElementById('topArtistsList');
    const searchList = document.getElementById('searchResultsList');

    loadTopArtists();

    let searchTimeout;
    searchInput.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        const query = searchInput.value.trim();
        clearSearch.style.display = query ? 'flex' : 'none';

        if (!query) {
            searchResults.style.display = 'none';
            defaultContent.style.display = 'block';
            return;
        }
        searchTimeout = setTimeout(() => searchArtists(query), 300);
    });

    clearSearch.addEventListener('click', () => {
        searchInput.value = '';
        clearSearch.style.display = 'none';
        searchResults.style.display = 'none';
        defaultContent.style.display = 'block';
    });

    document.addEventListener('click', (e) => {
        const row = e.target.closest('.track-row');
        if (row?.dataset.artistId) {
            window.location.href = `/artist/${row.dataset.artistId}/`;
        }
    });

    async function loadTopArtists() {
        try {
            const res = await fetch('/api/artists/top/');
            const data = await res.json();
            topList.innerHTML = renderArtists(data);
        } catch (err) {
            topList.innerHTML = '<p class="text-muted p-3">Ошибка загрузки</p>';
        }
    }

    async function searchArtists(query) {
        try {
            const res = await fetch(`/api/artists/search/?query=${encodeURIComponent(query)}`);
            const data = await res.json();
            defaultContent.style.display = 'none';
            searchResults.style.display = 'block';
            searchList.innerHTML = data.length ? renderArtists(data) : '<p class="text-muted p-3">Ничего не найдено</p>';
        } catch (err) {
            console.error(err);
        }
    }

    function renderArtists(artists) {
        if (!artists || artists.length === 0) {
            return '<p class="text-muted p-3">Артисты не найдены</p>';
        }
        return artists.map(a => `
            <div class="track-row" data-artist-id="${a.id}">
                ${a.avatar 
                    ? `<img src="${a.avatar}" class="track-row-cover" style="border-radius:50%;" alt="">`
                    : getDefaultCoverSVG('50', '50', '50%')}
                <div class="track-row-info">
                    <div class="track-row-title">${escapeHtml(a.name)}</div>
                    <div class="track-row-artist">${a.followers_count || 0} подписчиков</div>
                </div>
            </div>
        `).join('');
    }
});