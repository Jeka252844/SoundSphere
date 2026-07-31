import os
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from apps.tracks.models import Genre, Track
from apps.artists.models import Artist, Album
from apps.users.models import PlayList, PlayListTrack, PlayListLike, Follow
from apps.analitics.models import ListeningHistory
from mutagen.mp3 import MP3

User = get_user_model()

def run():
    # 1. ЖАНРЫ
    genres_data = [
        ('Rock', 'Рок', 'rock'),
        ('Jazz', 'Джаз', 'jazz'),
        ('Electronic', 'Электронная', 'electronic'),
        ('Hip-Hop', 'Хип-хоп', 'hiphop'),
        ('Classical', 'Классика', 'classical'),
    ]
    genres = []
    for name, display, slug in genres_data:
        g, _ = Genre.objects.get_or_create(name=name, defaults={'display': display, 'slug': slug})
        genres.append(g)
    print(f'Жанры: {Genre.objects.count()}')

    # 2. АРТИСТЫ
    artists = []
    artist_names = [
        'The Night Crows', 'DJ Neon Pulse', 'Acoustic Waves', 'Virtual Riot',
        'Luna Eclipse', 'SoundSphere Originals', 'Cyber Phoenix', 'Neon Dreams',
        'Midnight Echo', 'Silver Horizon'
    ]
    for i, name in enumerate(artist_names):
        try:
            username = f'artist_{i+1}'
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@soundsphere.com',
                    'is_artist': True
                }
            )
            user.set_password('artist123')
            user.save()

            artist, _ = Artist.objects.get_or_create(
                user=user,
                defaults={
                    'name': name,
                    'bio': f'{name} — независимый артист на SoundSphere. Создаёт уникальную музыку.'
                }
            )
            artists.append(artist)
        except Exception:
            pass
    print(f'Артисты: {Artist.objects.count()}')

    # 3. АЛЬБОМЫ 
    album_names = [
        'Midnight Drive', 'Neon Pulse', 'Acoustic Dreams',
        'Digital Horizon', 'Eclipse'
    ]
    albums = []
    for i, artist in enumerate(artists[:5]):
        try:
            album, _ = Album.objects.get_or_create(
                title=album_names[i],
                artist=artist,
                defaults={'release_date': datetime.now().date()}
            )
            albums.append(album)
        except Exception:
            pass
    print(f'Альбомы: {Album.objects.count()}')

    # 4. ТРЕКИ 
    main_artist = artists[5]
    track_data = [
        {
            'title': 'Сказочная тайга',
            'genre': genres[0],# Rock
            'audio_file': 'tracks/Agata_Kristi_-_Skazochnaya_tajjga_47829631.mp3',
            'cover': 'covers/2026-07-31_15-41-02.png'
        },
        {
            'title': 'Midnight Drive',
            'genre': genres[1],  # jazz
            'audio_file': 'tracks/Elvis_Presley_Herbie_Mann_Dzhordzh_Gershvin_-_Strike_Up_the_Band_47859153.mp3',
            'cover': 'covers/2026-07-31_15-41-02.png'
        },
        {
            'title': 'Neon Pulse',
            'genre': genres[2],
            'audio_file': 'tracks/Bon_Jovi_-_Its_My_Life_47852367.mp3'
        },
        {
            'title': 'Acoustic Sunset',
            'genre': genres[3],
            'audio_file': 'tracks/Rammstein_-_Du_Hast_63121920.mp3'
        },
        {
            'title': 'Classical Dawn',
            'genre': genres[4],
            'audio_file': 'tracks/Rammstein_-_Feuer_frei_57658984.mp3'
        },
    ]
    tracks = []
    for td in track_data:
        try:
            # Автоматический расчёт длительности
            file_path = os.path.join('media', td['audio_file'])
            duration = 180  # по умолчанию
            if os.path.exists(file_path):
                try:
                    audio = MP3(file_path)
                    duration = int(audio.info.length)
                except Exception:
                    pass

            track, created = Track.objects.get_or_create(
                title=td['title'],
                artist=main_artist,
                album=albums[0] if albums else None,
                genre=td['genre'],
                defaults={
                    'duration': duration,
                    'audio_file': td['audio_file'],
                    'cover': td.get('cover', '')
                }
            )
            if created:
                print(f'{track.title} ({duration}с)')
            tracks.append(track)
        except Exception as e:
            print(f'{td["title"]}: {e}')

    # 5. ПЛЕЙЛИСТЫ 
    playlists = []
    for i, artist in enumerate(artists[:5]):
        try:
            pl, _ = PlayList.objects.get_or_create(
                title=f'Плейлист {artist.name}',
                user=artist.user,
                defaults={'is_public': True}
            )
            playlists.append(pl)
        except Exception:
            pass

    # Добавляем треки в плейлисты
    for pl in playlists:
        try:
            for track in tracks:
                PlayListTrack.objects.get_or_create(playlist=pl, track=track)
        except Exception:
            pass
    print(f'Плейлисты: {PlayList.objects.count()}')

    # 6. 15 ПОЛЬЗОВАТЕЛЕЙ
    normal_users = []
    for i in range(15):
        try:
            username = f'user_{i+1}'
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@mail.com'}
            )
            user.set_password('user1234')
            user.save()
            normal_users.append(user)
        except Exception:
            pass
    print(f'Пользователи: {User.objects.count()}')

    # 7. ЛАЙКИ ПЛЕЙЛИСТАМ
    like_count = 0
    for user in normal_users:
        try:
            for pl in random.sample(list(playlists), random.randint(1, 3)):
                PlayListLike.objects.get_or_create(user=user, playlist=pl)
                like_count += 1
        except Exception:
            pass
    print(f'Лайки плейлистов: {like_count}')

    # 8. ПОДПИСКИ НА АРТИСТОВ
    follow_count = 0
    for user in normal_users:
        try:
            for artist in random.sample(artists, random.randint(1, 3)):
                Follow.objects.get_or_create(follower=user, following=artist)
                follow_count += 1
        except Exception:
            pass
    print(f'Подписки: {follow_count}')

    # 9. ПРОСЛУШИВАНИЯ
    listen_count = 0
    for user in normal_users:
        try:
            for track in random.sample(tracks, random.randint(1, len(tracks))):
                for _ in range(random.randint(1, 3)):
                    ListeningHistory.objects.create(
                        user=user,
                        track=track,
                        listened_at=datetime.now() - timedelta(days=random.randint(0, 6))
                    )
                    listen_count += 1
        except Exception:
            pass

    # Обновляем счётчики
    for track in tracks:
        try:
            track.plays_count = ListeningHistory.objects.filter(track=track).count()
            track.save()
        except Exception:
            pass
    print(f'Прослушивания: {listen_count}')

    User.objects.get_or_create(
        name='admin',
        user_role = 'admin',
        email = 'admin@ad.ad',
        password = 'admin123'
    )

    print('\nГОТОВО! Можно зайти как:')
    print('имя: artist_1, пароль: artist123. артист с песней, альбомом и плейлистом')
    print('имя: user_1, пароль: user1234. обычный пользователь')
    print('имя: admin, пароль: admin123. администратор')


if __name__ == '__main__':
    run()