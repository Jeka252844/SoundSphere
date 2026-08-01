document.addEventListener('DOMContentLoaded', () => {
    const logoShowcase = document.getElementById('logoShowcase');
    if (logoShowcase) {
        const logoGlow = logoShowcase.querySelector('.logo-glow');
        logoShowcase.addEventListener('mouseenter', () => logoGlow.style.opacity = '0.6');
        logoShowcase.addEventListener('mouseleave', () => logoGlow.style.opacity = '0.3');
    }

    const playBtn = document.getElementById('playBtn');
    if (playBtn) {
        playBtn.addEventListener('click', async () => {
            playBtn.style.transform = 'scale(0.95)';
            setTimeout(() => playBtn.style.transform = 'scale(1.05)', 150);

            const token = localStorage.getItem('access_token');
            if (token) {
                try {
                    const res = await fetch('/api/listening/current/', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (res.ok) {
                        const data = await res.json();
                        if (data.track_id) {
                            window.location.href = `/player/?track_id=${data.track_id}`;
                            return;
                        }
                    }
                } catch(e) {}
            }
            window.location.href = '/player/';
        });
    }
});