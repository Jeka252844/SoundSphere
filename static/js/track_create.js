document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        showMessageModal('Вы не авторизованы', 'Войдите в аккаунт', 'Войти', '/login/');
        return;
    }
    const urlParams = new URLSearchParams(window.location.search);
    const albumId = urlParams.get('album_id');

    const payload = JSON.parse(atob(token.split('.')[1]));
    const userId = payload.user_id;

    const listRes = await fetch('/api/artists/list/');
    const artists = await listRes.json();
    const myArtist = artists.find(a => a.user === userId);

    const albumSelect = document.getElementById('albumSelect');
    
    if (myArtist) {
        const artistRes = await fetch(`/api/artists/${myArtist.id}/`);
        const artist = await artistRes.json();

        if (artist.albums && artist.albums.length > 0) {
            albumSelect.innerHTML = '<option value="">Выберите альбом...</option>';
            artist.albums.forEach(album => {
                const option = document.createElement('option');
                option.value = album.id;
                option.textContent = album.title;
                if (album.id == albumId) option.selected = true;
                albumSelect.appendChild(option);
            });
        } else {
            albumSelect.innerHTML = '<option value="">Нет альбомов</option>';
        }

        const createAlbumBtn = document.createElement('button');
            createAlbumBtn.type = 'button';
            createAlbumBtn.className = 'btn btn-outline-secondary btn-sm mt-2 w-100';
            createAlbumBtn.textContent = '➕ Создать альбом';
            createAlbumBtn.onclick = () => window.location.href = '/album/create/';
            albumSelect.parentElement.appendChild(createAlbumBtn);
            
    } else {
        showMessageModal('Вы не артист', 'Создайте профиль артиста', 'Стать артистом', '/artist/create/');
    }

    const genreRes = await fetch('/api/tracks/genre/list/');
    const genres = await genreRes.json();

    const genreSelect = document.querySelector('select[name="genre"]');
    genreSelect.innerHTML = '<option value="">Выберите жанр...</option>';

    genres.forEach(genre => {
        const option = document.createElement('option');
        option.value = genre.id;
        option.textContent = genre.display || genre.name;
        genreSelect.appendChild(option);
    });

    // Отправка
    document.getElementById('trackCreateForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);

        const res = await fetch('/api/tracks/create/', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData
        });

        if (res.ok) {
            alert('Трек загружен!');
            window.location.replace(document.referrer || '/tracks/');
        } else {
            const data = await res.json();
            alert(Object.values(data).flat().join('\n'));
        }
    });
});