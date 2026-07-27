document.addEventListener('DOMContentLoaded', () => {
    const playBtn = document.querySelector('.play-button');
    const progressBar = document.querySelector('.progress-bar');
    const progress = progressBar.querySelector('.progress');
    const progressHandle = progressBar.querySelector('.progress-handle');
    const currentTimeEl = document.querySelector('.time-info span:first-child');
    const durationEl = document.querySelector('.time-info span:last-child');
    const trackId = document.querySelector('.audio-player').dataset.trackId;

    let socket = null;
    let isPlaying = false;
    let duration = 0;
    let mediaSource = null;
    let sourceBuffer = null;
    let audio = null;
    let progressInterval = null;
    let pendingChunks = [];
    let canPlay = false;
    let mimeType = 'audio/mpeg';

    let reconnectAttempts = 0;
    const maxReconnectAttempts = 3;
    let isReconnecting = false;
    let reconnectTimeout = null;

    loadTrackCover(trackId);

    async function loadTrackCover(trackId){
        const coverContainer = document.querySelector('.track-image');
        if (!coverContainer) return;

        try {
            const res = await fetch(`/api/tracks/${trackId}/`);
            const data = await res.json();

            if (data.cover) {
                coverContainer.innerHTML = `<img src="${data.cover}" class="track-row-cover" alt="">`;
            } else {
                coverContainer.innerHTML = getDefaultCoverSVG('80', '80', '100');
            }
        } catch (err) {
            coverContainer.innerHTML = getDefaultCoverSVG('90', '90', '100');
        }
    }

    function initMediaSource() {
        if (mediaSource && mediaSource.readyState === 'open') {
            try {
                if (sourceBuffer) mediaSource.removeSourceBuffer(sourceBuffer);
            } catch(e) {}
        }
        
        mediaSource = new MediaSource();
        audio = new Audio();
        audio.src = URL.createObjectURL(mediaSource);
        sourceBuffer = null;
        canPlay = false;
        pendingChunks = [];


        return new Promise((resolve) => {
            mediaSource.addEventListener('sourceopen', () => {
                console.log('MediaSource opened');
                sourceBuffer = mediaSource.addSourceBuffer(mimeType);
                
                sourceBuffer.addEventListener('updateend', () => {
                    processPendingChunks();
                    checkCanPlay();
                });
                
                initVolume();
                resolve();
            });
        });
    }

    function connectWebSocket() {
        if (socket) {
            socket.onclose = null;
            socket.close();
        }
        
        socket = new WebSocket(`ws://${window.location.host}/ws/player/`);

        socket.onopen = async () => {
            console.log('WebSocket connected');
            if (isReconnecting){
                reconnectAttempts = 0;
                isReconnecting = false;
                console.log('reconnecting successful');
            }
            socket.send(JSON.stringify({ command: 'play', track_id: parseInt(trackId) }));
        };

        socket.onmessage = (event) => {
            if (event.data instanceof Blob) {
                event.data.arrayBuffer().then(buf => {
                    if (!sourceBuffer) {
                        pendingChunks.push(buf);
                    } else if (!sourceBuffer.updating) {
                        sourceBuffer.appendBuffer(buf);
                    } else {
                        pendingChunks.push(buf);
                    }
                });
            } else {
                const data = JSON.parse(event.data);
                console.log(data.type);

                if (data.type === 'metadata') {
                    duration = data.duration;
                    durationEl.textContent = formatTime(duration);
                    if (data.mime_type) mimeType = data.mime_type;
                }

                if (data.type === 'end_of_stream') {
                    console.log('end_of_stream');
                    const tryEnd = () => {
                        if (sourceBuffer && !sourceBuffer.updating && pendingChunks.length === 0) {
                            if (mediaSource.readyState === 'open') {
                                mediaSource.endOfStream();
                                console.log('MediaSource ended');
                            }
                        } else {
                            setTimeout(tryEnd, 100);
                        }
                    };
                    tryEnd();
                }
            }
        };

        socket.onerror = (e) => console.error('WebSocket error');
        socket.onclose = () => {
            console.log('WebSocket closed');
            
            if (isPlaying && !isReconnecting){
                attemptReconnect();
            }
        };
    }

    function checkIfNeedsReconnect() {
        if (mediaSource && mediaSource.readyState === 'ended') {
            return false;
        }
        
        if (!sourceBuffer || !sourceBuffer.buffered || sourceBuffer.buffered.length === 0) {
            return true;
        }
        
        const bufferedEnd = sourceBuffer.buffered.end(sourceBuffer.buffered.length - 1);
        const currentPlayTime = audio ? audio.currentTime : 0;
        const remainingBuffer = bufferedEnd - currentPlayTime;
        
        console.log(`Buffer: ${remainingBuffer.toFixed(1)}s remaining`);
        
        if (remainingBuffer < 5) return true;
        
        if (bufferedEnd >= duration - 0.5) return false;
        
        return false;
    }

    function attemptReconnect() {
        if (reconnectAttempts >= maxReconnectAttempts) {
            console.log('Max reconnect attempts reached');
            isReconnecting = false;
            playBtn.innerHTML = '<i class="fas fa-exclamation-triangle fa-lg"></i>';
            setTimeout(() => {
                playBtn.innerHTML = isPlaying ? '<i class="fas fa-pause fa-lg"></i>' : '<i class="fas fa-play fa-lg"></i>';
            }, 2000);
            return;
        }

        reconnectAttempts++;
        isReconnecting = true;
        
        const delay = Math.pow(2, reconnectAttempts) * 1000;
        console.log(`Reconnect ${reconnectAttempts}/${maxReconnectAttempts} in ${delay/1000}s`);
        
        playBtn.innerHTML = '<i class="fas fa-spinner fa-spin fa-lg"></i>';
        
        reconnectTimeout = setTimeout(async () => {
            try {
                if (mediaSource && mediaSource.readyState === 'open') {
                    try {
                        if (sourceBuffer && sourceBuffer.updating) {
                            await new Promise((resolve) => {
                                sourceBuffer.addEventListener('updateend', () => resolve(), { once: true });
                            });
                        }
                        if (sourceBuffer) {
                            mediaSource.removeSourceBuffer(sourceBuffer);
                            console.log('Old SourceBuffer removed');
                        }
                        mediaSource.endOfStream();
                        console.log('Old MediaSource ended');
                    } catch(e) {
                        console.log('Cleanup error:', e.message);
                    }
                }
                
                await initMediaSource();
                
                connectWebSocket();
                
                const wait = setInterval(() => {
                    if (canPlay && !sourceBuffer.updating) {
                        clearInterval(wait);
                        audio.play();
                        console.log('Resumed after reconnect!');
                        playBtn.innerHTML = '<i class="fas fa-pause fa-lg"></i>';
                    }
                }, 200);
                
                setTimeout(() => clearInterval(wait), 15000);
                
            } catch (e) {
                console.error('Reconnect failed:', e);
                isReconnecting = false;
                playBtn.innerHTML = '<i class="fas fa-play fa-lg"></i>';
            }
        }, delay);
    }

    function cancelReconnect() {
        if (reconnectTimeout) {
            clearTimeout(reconnectTimeout);
            reconnectTimeout = null;
        }
        isReconnecting = false;
        reconnectAttempts = 0;
    }

    function processPendingChunks() {
        if (!sourceBuffer || sourceBuffer.updating || pendingChunks.length === 0) return;
        const chunk = pendingChunks.shift();
        sourceBuffer.appendBuffer(chunk);
    }

    function checkCanPlay() {
        if (!sourceBuffer || !sourceBuffer.buffered || sourceBuffer.buffered.length === 0) return;
        const bufferedEnd = sourceBuffer.buffered.end(sourceBuffer.buffered.length - 1);
        if (bufferedEnd >= 2 || bufferedEnd >= duration - 0.5) {
            canPlay = true;
            console.log('Can play! Buffer:', bufferedEnd.toFixed(1) + 's');
        }
    }

    function formatTime(seconds) {
        if (isNaN(seconds)) return '0:00';
        const m = Math.floor(seconds / 60);
        const s = Math.floor(seconds % 60);
        return `${m}:${s.toString().padStart(2, '0')}`;
    }

    function updateProgress() {
        if (!isPlaying || !audio) return;
        currentTimeEl.textContent = formatTime(audio.currentTime);
        if (duration > 0) {
            const pct = (audio.currentTime / duration) * 100;
            progress.style.width = pct + '%';
            progressHandle.style.left = pct + '%';
        }
    }

    playBtn.addEventListener('click', async () => {
        if (isPlaying) {
            cancelReconnect();
            audio.pause();
            clearInterval(progressInterval);
            isPlaying = false;
            playBtn.innerHTML = '<i class="fas fa-play fa-lg"></i>';
            return;
        }

        // Новое соединение
        const needNew = !socket || 
            socket.readyState !== WebSocket.OPEN || 
            (mediaSource && mediaSource.readyState !== 'open');

        if (needNew) {
            playBtn.innerHTML = '<i class="fas fa-spinner fa-spin fa-lg"></i>';
            
            // Пересоздаём всё
            await initMediaSource();
            initVolume();
            connectWebSocket();
            
            // Ждём буферизации
            const wait = setInterval(() => {
                if (canPlay && !sourceBuffer.updating) {
                    clearInterval(wait);
                    audio.play();
                    progressInterval = setInterval(updateProgress, 200);
                    isPlaying = true;
                    playBtn.innerHTML = '<i class="fas fa-pause fa-lg"></i>';
                    console.log('Playing!');
                }
            }, 200);
            
            setTimeout(() => clearInterval(wait), 15000);
        } else {
            audio.play();
            progressInterval = setInterval(updateProgress, 200);
            isPlaying = true;
            playBtn.innerHTML = '<i class="fas fa-pause fa-lg"></i>';
        }
    });

    progressBar.addEventListener('click', (e) => {
        if (!audio || !duration) return;
        const rect = progressBar.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        audio.currentTime = percent * duration;
    });

    console.log('Player ready, trackId:', trackId);

    // ============================================
    // ГРОМКОСТЬ
    const volumeBtn = document.querySelector('.volume-control .control-button');
    const volumeSlider = document.querySelector('.volume-slider');
    const volumeLevel = document.querySelector('.volume-level');

    let savedVolume = localStorage.getItem('soundsphere_volume');
    if (savedVolume === null) savedVolume = 0.7; 
    else savedVolume = parseFloat(savedVolume);

    let volumeInitialized = false;

    function initVolume() {
        if (volumeInitialized || !audio) return;
        volumeInitialized = true;
        
        audio.volume = savedVolume;
        updateVolumeUI();
    }

    // ползунк громкости
    volumeSlider.addEventListener('click', (e) => {
        const rect = volumeSlider.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        setVolume(percent);
    });

    // Кнопка mute/unmute
    volumeBtn.addEventListener('click', () => {
        if (!audio) return;
        if (audio.muted) {
            audio.muted = false;
        } else {
            audio.muted = true;
        }
        updateVolumeUI();
    });

    function setVolume(value) {
        if (!audio) return;
        audio.volume = Math.max(0, Math.min(1, value));
        audio.muted = false;
        localStorage.setItem('soundsphere_volume', audio.volume);
        updateVolumeUI();
    }

    function updateVolumeUI() {
        if (!audio) return;
        if (audio.muted) {
            volumeBtn.innerHTML = '<i class="fas fa-volume-mute fa-lg"></i>';
            volumeLevel.style.width = '0%';
        } else {
            const vol = audio.volume;
            volumeLevel.style.width = (vol * 100) + '%';
            
            if (vol === 0) {
                volumeBtn.innerHTML = '<i class="fas fa-volume-mute fa-lg"></i>';
            } else if (vol < 0.5) {
                volumeBtn.innerHTML = '<i class="fas fa-volume-down fa-lg"></i>';
            } else {
                volumeBtn.innerHTML = '<i class="fas fa-volume-up fa-lg"></i>';
            }
        }
    }
});