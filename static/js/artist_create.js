document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        showMessageModal('Вы не авторизованы', 'Войдите в аккаунт', 'Войти', '/login/');
        return;
    }

    // Отправка
    document.getElementById('artistCreateForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);

        const res = await fetch('/api/artists/create/', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData
        });

        if (res.ok) {
            alert('Артист создан!');
            window.location.replace(document.referrer || '/artist/my/');
        } else {
            const data = await res.json();
            alert(Object.values(data).flat().join('\n'));
        }
    });
});