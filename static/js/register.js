document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    if (!registerForm) {
        alert('Данные не найдены');
        return;
    }

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
            alert("Регистрация успешна");
            window.location.href = '/login/';
        } else {
            const data = await response.json();
            alert(Object.values(data).flat().join('\n'));
        }
    });
});