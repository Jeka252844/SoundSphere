document.addEventListener('DOMContentLoaded', () => {
    const logoShowcase = document.getElementById('logoShowcase');
    if (!logoShowcase) return;
    
    const logoGlow = logoShowcase.querySelector('.logo-glow');
    logoShowcase.addEventListener('mouseenter', () => {
        logoGlow.style.opacity = '0.6';
    });
    logoShowcase.addEventListener('mouseleave', () => {
        logoGlow.style.opacity = '0.3';
    });

    const playBtn = document.getElementById('playBtn');
    if (playBtn) {
		playBtn.addEventListener('click', () => {
			playBtn.style.transform = 'scale(0.95)';
			setTimeout(() => {
				playBtn.style.transform = 'scale(1.05)';
				alert('Запуск платформы SoundSphere (Django Vanilla Edition)...');
			}, 150);
		});
	}

	console.log('%c SoundSphere Vanilla JS initialized! ', 'background: #092E20; color: #44B78B; font-weight: bold; padding: 4px;');
});
