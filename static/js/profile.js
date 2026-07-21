document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');
    if (!token){
        window.location.href = '/login/';
        return;
    }

    const payload = JSON.parse(atob(token.split('.')[1]));
    const userId = payload.user_id;
    const response = await fetch(`/users/${userId}/`, {
        headers: {'Authorization': `Bearer ${token}`}
    });
    const user = await response.json();

    document.getElementById('profileUsername').textContent = user.username;
    document.getElementById('profileEmail').textContent = user.email || '-';
    document.getElementById('profilePhone').textContent = user.phone_number || '-';
    document.getElementById('profileName').textContent = user.username;
    document.getElementById('profileRole').textContent = user.user_role;
    document.getElementById('profileBioText').textContent = user.bio || '-';
    document.getElementById('userAvatar').src = user.avatar || "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3.webp"

    const deleteProfileBtn = document.getElementById('deleteProfileBtn');
    const editProfileBtn = document.getElementById('editProfileBtn');
    const profileInfo = document.getElementById('profileInfo');
    const profileEdit = document.getElementById('profileEdit');
    const cancelEditBtn = document.getElementById('cancelEditBtn');
    const profileEditForm = document.getElementById('profileEditForm');
    const avatarInput = document.getElementById('avatarInput');

    const username = document.getElementById('profileUsername').textContent;
    const email = document.getElementById('profileEmail').textContent;
    const phone = document.getElementById('profilePhone').textContent;
    const bio = document.getElementById('profileBioText').textContent;
    
    editProfileBtn.addEventListener('click', () => {
        profileInfo.style.display = 'none';
        profileEdit.style.display = 'block';

        document.getElementById('editUsername').value = username;
        document.getElementById('editEmail').value = email;
        document.getElementById('editPhone').value = phone;
        document.getElementById('editBio').value = bio;
    });

    cancelEditBtn.addEventListener('click', ()=>{
        profileInfo.style.display = 'block';
        profileEdit.style.display = 'none';
    });

    profileEditForm.addEventListener('submit', async (e) =>{
        e.preventDefault();
        
        const formData = new FormData();

        if (username !== document.getElementById('editUsername').value){
            formData.append('username', document.getElementById('editUsername').value);
        }
        if (email !== document.getElementById('editEmail').value){
            formData.append('email', document.getElementById('editEmail').value);
        }
        if (phone !== document.getElementById('editPhone').value){
            formData.append('phone_number', document.getElementById('editPhone').value);
        }
        if (bio !== document.getElementById('editBio').value){
            formData.append('bio', document.getElementById('editBio').value);
        }
        
        if (avatarInput.files[0]) {
            formData.append('avatar', avatarInput.files[0]);
        }

        const response = await fetch('/users/update/', {
            method: 'PATCH',
            headers: {'Authorization': `Bearer ${token}`},
            body: formData
        });

        if (response.ok) {
            location.reload();
        } else  {
            const error = await response.json();
            alert(Object.values(error).flat().join('\n'));
            return;
        }
        
    });

    deleteProfileBtn.addEventListener('click', async () => {
        ok = confirm('Вы точно хотите удалить аккаунт. После удаления его невозможно будет востановить.');
        if (ok){
            const response = await fetch(`/users/${userId}/delete/`, {
                method: 'DELETE',
                headers: {'Authorization': `Bearer ${token}`}
            });
            if (response.ok){
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/';
            }
        }
    });
}); 
