document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');
    const loginBtn = document.getElementById('loginBtn');

    if (token) {
        if (loginBtn) loginBtn.style.display = 'none';
    } else {
        if (loginBtn) loginBtn.style.display = 'flex';
    }

    const profileBtn = document.getElementById('profileBtn');
    const sidePanel = document.getElementById('sidePanel');
    const sidePanelOverlay = document.getElementById('sidePanelOverlay');
    const closePanel = document.getElementById('closePanel');
    const logoutBtn = document.getElementById('logoutBtn');

    // Открыть панель
    if (profileBtn) {
        profileBtn.addEventListener('click', () => {
            sidePanel.classList.add('active');
            sidePanelOverlay.classList.add('active');
            loadPanelUserInfo();
        });
    }

    // Закрыть панель
    function closeSidePanel() {
        sidePanel.classList.remove('active');
        sidePanelOverlay.classList.remove('active');
    }

    if (closePanel) closePanel.addEventListener('click', closeSidePanel);
    if (sidePanelOverlay) sidePanelOverlay.addEventListener('click', closeSidePanel);

    async function loadPanelUserInfo() {
        const token = localStorage.getItem('access_token');
        
        if (token) {
            try {
                const payload = JSON.parse(atob(token.split('.')[1]));
                const userId = payload.user_id;
                const res = await fetch(`/users/${userId}/`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                const user = await res.json();
                
                document.getElementById('panelUsername').textContent = user.username;
                document.getElementById('panelEmail').textContent = user.email || '';
                
                // Показываем кнопку "Выйти"
                if (logoutBtn) logoutBtn.style.display = 'flex';

                if (user.user_role === 'moderator') {
                    const adminLink = document.getElementById('adminPanelLink');
                    if (adminLink) {
                        adminLink.style.display = 'flex';
                        adminLink.href = '/moderator/'; 
                    }
                }

                if (user.user_role === 'admin') {
                    const adminLink = document.getElementById('adminPanelLink');
                    if (adminLink) {
                        adminLink.style.display = 'flex';
                        adminLink.href = '/admin/'; 
                    }
                }
                
                document.querySelectorAll('.auth-required').forEach(el => {
                    el.classList.remove('locked');
                });
                
            } catch (err) {
                setGuestMode();
            }
        } else {
            setGuestMode();
        }
    }

    function setGuestMode() {
        document.getElementById('panelUsername').textContent = 'Гость';
        if (logoutBtn) logoutBtn.style.display = 'none';
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            const ok = confirm('Вы точно хотите выйти из аккаунта?')
            if (ok){
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/';
            } 
            return;
        });
    }

    // Закрыть по Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeSidePanel();
    });
});