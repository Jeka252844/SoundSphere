document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');
    const artistId = ARTIST_ID;
    const isMy = IS_MY;

    let artist = null;
    let isOwner = false;

    if (isMy) {
        if (!token) {
            showMessageModal('Вы не авторизованы', 'Войдите в аккаунт', 'Войти', '/login/');
            return;
        }

        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const userId = payload.user_id;

            const userRes = await fetch(`/users/${userId}/`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const user = await userRes.json();

            if (!user.is_artist) {
                showMessageModal('Вы не артист', 'Создайте профиль артиста', 'Стать артистом', '/artist/create/');
                return;
            }

            const listRes = await fetch('/api/artists/list/');
            const artists = await listRes.json();
            artist = artists.find(a => a.user === userId);

            if (!artist) {
                showMessageModal('Ошибка', 'Профиль артиста не найден', 'Создать артиста', '/artist/create/');
                return;
            }


            isOwner = true;
            renderArtistProfile(artist, isOwner, token);

        } catch (err) {
            console.log(err)
            showMessageModal('Ошибка загрузки', '', 'Назад', 'back');
        }
        return;
    }

    if (artistId) {
        try {
            const res = await fetch(`/api/artists/${artistId}/`);
            artist = await res.json();

            // Проверяем: мой артист?
            if (token) {
                const payload = JSON.parse(atob(token.split('.')[1]));
                const userId = payload.user_id;
                const listRes = await fetch('/api/artists/list/');
                const artists = await listRes.json();
                const myArtist = artists.find(a => a.user === userId);
                if (myArtist && myArtist.id === artist.id) {
                    isOwner = true;
                }
            }

            renderArtistProfile(artist, isOwner, token);

        } catch (err) {
            console.log(err);
            showMessageModal('Артист не найден', '', 'Назад', 'back');
        }
        return;
    }

    showMessageModal('Произошла какая-то ошибка', '', 'Назад', 'back');
});


async function renderArtistProfile(artist, isOwner, token) {
    document.getElementById('artistName').textContent = artist.name;
    document.getElementById('artistBio').textContent = artist.bio || 'Описания пока нет';
    document.getElementById('artistFollowers').textContent = `${artist.followers_count || 0} подписчиков`;

    // Аватар
    const avatarContainer = document.getElementById('artistAvatarContainer');
    if (artist.avatar) {
        avatarContainer.innerHTML = `<img src="${artist.avatar}" class="artist-avatar" alt="">`;
    } else {
        avatarContainer.innerHTML = getDefaultCoverSVG('120', '120', '100%');
    }
    const svg = avatarContainer.querySelector('svg');
    if (svg) {
        svg.classList.add('artist-avatar');
        svg.style.width = '120px';
        svg.style.height = '120px';
    }

    const avatarEl = document.getElementById('artistAvatarContainer');
    if (avatarEl) {
        avatarEl.style.cursor = 'pointer';
        avatarEl.addEventListener('click', () => {
            const modal = document.getElementById('avatarModal');
            const modalImg = document.getElementById('avatarModalImg');
            modal.style.display = 'flex';
            modalImg.src = artist.avatar || '';
        });
    }

    // Закрыть модалку
    document.getElementById('closeAvatarModal').addEventListener('click', () => {
        document.getElementById('avatarModal').style.display = 'none';
    });

    // Клик вне — закрыть
    document.getElementById('avatarModal').addEventListener('click', (e) => {
        if (e.target === e.currentTarget) {
            e.currentTarget.style.display = 'none';
        }
    });

    // cvtybnm fdfnfh
    document.getElementById('changeAvatarBtn').addEventListener('click', () => {
        document.getElementById('avatarFileInput').click();
    });

    document.getElementById('avatarFileInput').addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        const formData = new FormData();
        formData.append('avatar', file);
        
        const token = localStorage.getItem('access_token');
        const res = await fetch('/api/artists/update/', {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData
        });
        
        if (res.ok) {
            const data = await res.json();
            document.getElementById('avatarModalImg').src = data.avatar;
            const avatarContainer = document.getElementById('artistAvatarContainer');
            avatarContainer.innerHTML = `<img src="${data.avatar}" class="artist-avatar" alt="">`;
        }
    });
    
    // Поделиться
    document.getElementById('shareBtn').addEventListener('click', () => {
        const shareUrl = isOwner 
            ? `${window.location.origin}/artist/${artist.id}/`
            : window.location.href;
        navigator.clipboard.writeText(shareUrl).then(() => alert('Ссылка скопирована'));
    });

    // Альбомы
    const albumsList = document.getElementById('albumsList');
    if (artist.albums && artist.albums.length > 0) {
        albumsList.innerHTML = artist.albums.map(album => `
            <div class="track-row" data-album-id="${album.id}">
                ${album.cover ? `<img src="${album.cover}" class="track-row-cover" alt="">` : getDefaultCoverSVG('50','50','8')}
                <div class="track-row-info">
                    <div class="track-row-title">${escapeHtml(album.title)}</div>
                    <div class="track-row-artist">${album.release_date || ''}</div>
                </div>
            </div>
        `).join('');
    } else {
        albumsList.innerHTML = '<p class="p-3">Нет альбомов</p>';
    }

    document.addEventListener('click', (e) => {
        const row = e.target.closest('.track-row');
        if (row?.dataset.albumId) {
            window.location.href = `/album/${row.dataset.albumId}/`;
        }
    });

    // КНОПКИ
    const actionsDiv = document.querySelector('.artist-actions');
    if (isOwner) {
        actionsDiv.innerHTML = `
            <button class="btn btn-outline-secondary btn-sm" id="editArtistBtn">
                <i class="fas fa-pen"></i> Редактировать
            </button>
            <button class="btn btn-outline-secondary btn-sm" id="shareBtn">
                <i class="fas fa-share"></i> Поделиться
            </button>
            <button class="btn btn-outline-danger btn-sm" id="deleteArtistBtn">
                <i class="fas fa-trash"></i> Удалить
            </button>
        `;

        document.getElementById('deleteArtistBtn').addEventListener('click', async () => {
            if (!confirm('Удалить профиль артиста?')) return;
            const token = localStorage.getItem('access_token');
            const res = await fetch(`/api/artists/${artist.id}/delete/`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                alert('Профиль удалён');
                window.location.href = '/profile/';
            }
        });
        document.getElementById('editArtistBtn').addEventListener('click', () => {
            document.getElementById('editArtistName').value = artist.name || '';
            document.getElementById('editArtistBio').value = artist.bio || '';
            document.getElementById('editArtistError').style.display = 'none';
            document.getElementById('editArtistModal').style.display = 'flex';
        });

        // Закрыть
        document.getElementById('closeEditModal').addEventListener('click', () => {
            document.getElementById('editArtistModal').style.display = 'none';
        });
        document.getElementById('cancelEditBtn').addEventListener('click', () => {
            document.getElementById('editArtistModal').style.display = 'none';
        });

        // сохранить
        document.getElementById('saveArtistBtn').addEventListener('click', async () => {
            const name = document.getElementById('editArtistName').value.trim();
            const bio = document.getElementById('editArtistBio').value.trim();
            const errorDiv = document.getElementById('editArtistError');
            
            if (!name) {
                errorDiv.textContent = 'Имя обязательно';
                errorDiv.style.display = 'block';
                return;
            }
            
            const token = localStorage.getItem('access_token');
            const res = await fetch('/api/artists/update/', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ name, bio })
            });
            
            if (res.ok) {
                document.getElementById('artistName').textContent = name;
                document.getElementById('artistBio').textContent = bio || 'Описания пока нет';
                document.getElementById('editArtistModal').style.display = 'none';
            } else {
                const data = await res.json();
                errorDiv.textContent =(data.name?.[0] || data.bio?.[0] || 'Ошибка');
                errorDiv.style.display = 'block';
            }
        });

        const createAlbumBtn = document.createElement('button');
        createAlbumBtn.className = 'btn btn-outline-secondary btn-sm mt-2';
        createAlbumBtn.innerHTML = '<i class="fas fa-plus"></i> Создать альбом';
        createAlbumBtn.onclick = () => window.location.href = '/album/create/';
        albumsList.parentElement.appendChild(createAlbumBtn);

    } else {
        actionsDiv.innerHTML = `
            <button class="btn btn-primary btn-sm" id="followBtn">
                <i class="fas fa-user-plus"></i> Подписаться
            </button>
            <button class="btn btn-outline-secondary btn-sm" id="shareBtn">
                <i class="fas fa-share"></i> Поделиться
            </button>
        `;

        // Подписка
        document.getElementById('followBtn').addEventListener('click', async () => {
            const token = localStorage.getItem('access_token');
            if (!token) return alert('Войдите чтобы подписаться');
            const res = await fetch(`/users/${artist.id}/follow/`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await res.json();
            document.getElementById('followBtn').innerHTML = 
                data.status === 'followed' 
                    ? '<i class="fas fa-check"></i> Вы подписаны' 
                    : '<i class="fas fa-user-plus"></i> Подписаться';
        });
    }

    if (!isOwner && token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const userId = payload.user_id;
            const followRes = await fetch(`/api/artists/${artist.id}/follow/check/?user_id=${userId}`);
            const followData = await followRes.json();
            
            if (followData.is_following) {
                document.getElementById('followBtn').innerHTML = '<i class="fas fa-check"></i> Вы подписаны';
            }
        } catch(e) {}
    }
}

function getUserId(token) {
    return JSON.parse(atob(token.split('.')[1])).user_id;
}