document.addEventListener('DOMContentLoaded', async () => {
    if (localStorage.getItem('access_token')){
        document.getElementById('loginBtn').style.display = 'none'
        document.getElementById('profileBtn').style.display = 'block'
    } 
});