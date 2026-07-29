let currentUser = null;

function closePasswordModal() {
    document.getElementById('passwordModal').style.display = 'none';
}

function editField(field) {
    document.getElementById(`editRow-${field}`).style.display = 'flex';
    const input = document.getElementById(`edit${field.charAt(0).toUpperCase() + field.slice(1)}`);
    if (input) {
        const key = field === 'phone' ? 'phone_number' : field;
        input.value = currentUser[key] || '';
        input.focus();
    }
}

function cancelField(field) {
    document.getElementById(`editRow-${field}`).style.display = 'none';
}

async function saveField(field) {
    const token = localStorage.getItem('access_token');
    const input = document.getElementById(`edit${field.charAt(0).toUpperCase() + field.slice(1)}`);
    let value = input?.value.trim();
    
    const key = field === 'phone' ? 'phone_number' : field;
    
    if (value === '') value = null;
    
    const res = await fetch('/users/update/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ [key]: value })
    });
    
    if (res.ok) {
        currentUser[key] = value;
        const displayId = field === 'bio' ? 'profileBioText' : `profile${field.charAt(0).toUpperCase() + field.slice(1)}`;
        document.getElementById(displayId).textContent = value || '—';
        cancelField(field);
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login/';
        return;
    }

    const payload = JSON.parse(atob(token.split('.')[1]));
    const userId = payload.user_id;
    const response = await fetch(`/users/${userId}/`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const user = await response.json();
    
    currentUser = user;

    document.getElementById('profileUsername').textContent = user.username;
    document.getElementById('profileEmail').textContent = user.email || '-';
    document.getElementById('profilePhone').textContent = user.phone_number || '-';
    document.getElementById('profileName').textContent = user.username;
    document.getElementById('profileRole').textContent = user.user_role;
    document.getElementById('profileBioText').textContent = user.bio || '-';
    document.getElementById('userAvatar').src = user.avatar || "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3.webp";

    const avatarEl = document.getElementById('userAvatar');
    const avatarInput = document.getElementById('avatarInput');

    if (avatarEl && avatarInput) {
        avatarEl.addEventListener('click', () => avatarInput.click());
        
        avatarInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;
            
            const formData = new FormData();
            formData.append('avatar', file);
            
            const res = await fetch('/users/update/', {
                method: 'PUT',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData
            });
            
            if (res.ok) {
                const data = await res.json();
                avatarEl.src = data.avatar;
            }
        });
    }

    document.getElementById('deleteProfileBtn').addEventListener('click', async () => {
        const ok = confirm('Вы точно хотите удалить аккаунт?');
        if (ok) {
            const response = await fetch(`/users/${userId}/delete/`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/';
            }
        }
    });

    document.getElementById('changePasswordBtn').addEventListener('click', () => {
        document.getElementById('passwordModal').style.display = 'flex';
        document.getElementById('oldPassword').value = '';
        document.getElementById('newPassword1').value = '';
        document.getElementById('newPassword2').value = '';
        document.getElementById('passwordError').style.display = 'none';
    });


    document.getElementById('passwordModal').addEventListener('click', (e) => {
        if (e.target === e.currentTarget) closePasswordModal();
    });

    document.getElementById('submitPassword').addEventListener('click', async () => {
        const oldPass = document.getElementById('oldPassword').value;
        const newPass1 = document.getElementById('newPassword1').value;
        const newPass2 = document.getElementById('newPassword2').value;
        const errorDiv = document.getElementById('passwordError');
        
        // Проверки
        if (!oldPass || !newPass1 || !newPass2) {
            errorDiv.textContent = 'Заполните все поля';
            errorDiv.style.display = 'block';
            return;
        }
        
        if (newPass1 !== newPass2) {
            errorDiv.textContent = 'Пароли не совпадают';
            errorDiv.style.display = 'block';
            return;
        }
        
        const token = localStorage.getItem('access_token');
        const response = await fetch('/users/password/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ 
                old_password: oldPass, 
                new_password: newPass1 
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Пароль успешно изменён');
            closePasswordModal();
        } else {
            errorDiv.textContent =(data.error || 'Ошибка');
            errorDiv.style.display = 'block';
        }
    });
});