function getDefaultCoverSVG(width, height, radius) {
    return `
    <svg width="${width}" height="${height}" viewBox="0 0 400 400" 
        class="track-row-cover default-cover-svg" 
        style="border-radius:${radius}px;flex-shrink:0;">
        <defs>
            <radialGradient id="bg${width}" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#092E20"/>
                <stop offset="100%" stop-color="#040D09"/>
            </radialGradient>
            <linearGradient id="wv${width}" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#44B78B"/>
                <stop offset="50%" stop-color="#55cda0"/>
                <stop offset="100%" stop-color="#25865C"/>
            </linearGradient>
        </defs>
        <rect width="400" height="400" fill="url(#bg${width})"/>
        <circle cx="200" cy="200" r="140" fill="none" stroke="#25865C" stroke-width="1" stroke-dasharray="4 8" opacity="0.5"/>
        <circle cx="200" cy="200" r="100" fill="none" stroke="#44B78B" stroke-width="2" opacity="0.3"/>
        <path d="M 0 200 Q 100 80 200 200 T 400 200" fill="none" stroke="url(#wv${width})" stroke-width="8" stroke-linecap="round"/>
        <path d="M 0 200 Q 100 320 200 200 T 400 200" fill="none" stroke="#25865C" stroke-width="4" stroke-linecap="round" opacity="0.6"/>
        <circle cx="200" cy="200" r="8" fill="#55cda0"/>
    </svg>`;
}

function formatDuration(seconds) {
    if (!seconds || isNaN(seconds)) return '0:00';
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
}

function formatPlays(count) {
    if (count >= 1000000) return (count / 1000000).toFixed(1) + 'M';
    if (count >= 1000) return (count / 1000).toFixed(1) + 'K';
    return String(count);
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showMessageModal(title, message, buttonText, buttonUrl) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.style.display = 'flex';
    overlay.innerHTML = `
        <div class="modal-content" style="max-width:400px;text-align:center;">
            <div class="modal-body" style="padding:2rem;">
                <div style="font-size:2.5rem;margin-bottom:0.75rem;">⚠️</div>
                <h3 style="color:#fff;margin-bottom:0.5rem;">${title}</h3>
                <p >${message}</p>
                <button class="btn btn-primary mt-3" id="modalActionBtn">${buttonText}</button>
            </div>
        </div>
    `;
    document.body.appendChild(overlay);

    document.getElementById('modalActionBtn').addEventListener('click', () => {
        overlay.remove();
        if (buttonUrl === 'back') {
            history.back();
        } else if (buttonUrl) {
            window.location.href = buttonUrl;
        }
    });

    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            overlay.remove();
            if (history.length > 1) {
                history.back();
            } else {
                window.location.href = '/';
            }
        }
    });

}

function showReportModal(type, targetId, targetName) {
    const token = localStorage.getItem('access_token');
    const modal = document.getElementById('reportModal');
    
    modal.innerHTML = `
        <div class="modal-content" style="max-width:440px;">
            <div class="modal-header">
                <h3> Жалоба</h3>
                <button class="modal-close" id="closeReportModal">✕</button>
            </div>
            <div class="modal-body">
                <p class="modal-track-name">${targetName}</p>
                <label class="report-label">Причина:</label>
                <select id="reportReason" class="report-select">
                    <option value="">Выберите причину...</option>
                    <option value="copyright">Нарушение авторских прав</option>
                    <option value="inappropriate">Неприемлемый контент</option>
                    <option value="spam">Спам</option>
                    <option value="fake">Подделка</option>
                    <option value="other">Другое</option>
                </select>
                <label class="report-label">Описание:</label>
                <textarea id="reportDescription" class="report-textarea" rows="3" placeholder="Опишите проблему..."></textarea>
            </div>
            <div class="modal-footer">
                <button class="btn btn-sm btn-outline-secondary" id="cancelReport">Отмена</button>
                <button class="btn btn-sm btn-success" id="submitReport">Отправить</button>
            </div>
        </div>
    `;
    modal.style.display = 'flex';

    function close() { modal.style.display = 'none'; }

    document.getElementById('closeReportModal').addEventListener('click', close);
    document.getElementById('cancelReport').addEventListener('click', close);
    modal.addEventListener('click', (e) => { if (e.target === modal) close(); });

    document.getElementById('submitReport').addEventListener('click', async () => {
        const reason = document.getElementById('reportReason').value;
        const description = document.getElementById('reportDescription').value;
        if (!reason) return alert('Выберите причину');

        const res = await fetch('/api/social/report/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                type: type,
                target_id: targetId,
                reason,
                description
            })
        });

        if (res.ok) {
            alert('Жалоба отправлена');
            close();
        }
    });
}