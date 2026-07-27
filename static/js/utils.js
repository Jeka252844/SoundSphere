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
