document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');

    if (!token) {
        showMessageModal('Вы не авторизованы', 'Войдите в аккаунт', 'Войти', '/login/');
        return;
    }

    document.getElementById('albumCreateForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        const res = await fetch('/api/artists/album/create/', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData
        });

        if (res.ok) {
            const data = await res.json();
            window.location.href = `/album/${data.id}/`;
        } else {
            const data = await res.json();
            alert(Object.values(data).flat().join('\n'));
        }
    });
});