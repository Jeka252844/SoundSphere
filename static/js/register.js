document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    if (!registerForm) return;

    registerForm.addEventListener('submit', async function(e){
        e.preventDefault();

        if (this.password.value != this.password2.value){
            alert('Пароли не совпадают');
            return;
        }

        const response = await fetch('/users/create/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                username: this.username.value,
                email: this.email.value,
                password: this.password.value
            })
        });
        
        if (response.ok){
            const email = this.email.value;
            registerForm.style.display = 'none';
            document.getElementById('verifyEmail').textContent = email;
            document.getElementById('verifyModal').style.display = 'flex';

            const checkInterval = setInterval(() => {
                if (localStorage.getItem('email_verified') === 'true') {
                    localStorage.removeItem('email_verified');
                    clearInterval(checkInterval);
                    alert('Регистрация успешно завершена!');
                    window.location.href = '/login/';
                }
            }, 2000);
        } else {
            const data = await response.json();
            alert(Object.values(data).flat().join('\n'));
        }
    });
});