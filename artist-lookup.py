import requests
import webbrowser


def search_artists(artist_name):
    search_url = f'https://itunes.apple.com/search?term={artist_name}&entity=musicArtist'
    response = requests.get(search_url)
    data = response.json()
    artists = []
    if 'results' in data and len(data['results']) > 0:
        for artist in data['results']:
            artists.append([artist['artistName'], artist['artistId']])
    return artists

def get_albums(artist_ID):
    search_url = f'https://itunes.apple.com/lookup?id={artist_ID}&entity=album'
    response = requests.get(search_url)
    data = response.json()
    albums = []
    if 'results' in data and len(data['results']) > 0:
        for album in data['results']:
            if 'collectionType' in album and album['collectionType'] == 'Album':
                albums.append([album['collectionName'], album['collectionId']])
    return albums

def get_songs(album_ID):
    search_url = f'https://itunes.apple.com/lookup?id={album_ID}&entity=song'
    response = requests.get(search_url)
    data = response.json()
    songs = []
    if 'results' in data and len(data['results']) > 0:
        for song in data['results']:
            if 'trackName' in song and 'trackTimeMillis' in song:
                songs.append([song['trackName'], song['trackId'], song['trackTimeMillis']])
    return songs

def main():
    artist_name = input('Please enter the name of an artist:\n')
    artists = search_artists(artist_name)
    if len(artists) == 1:
        print('1 artist found.')
    else:
        print(f'{len(artists)} artists found.')
    print('Artists:')
    for num, artist in enumerate(artists, start=1):
        print(f'{num}: {artist[0]}')
    artist_num = int(input('Select an artist with their number.\n')) - 1
    print(f'You selected: {artists[artist_num][0]}')
    print(artists[artist_num][1])
    artist_name = artists[artist_num][0]

    albums = get_albums(artists[artist_num][1])
    if len(albums) == 1:
        print('1 album found.')
    else:
        print(f'{len(albums)} albums found.')
        print(f'{artist_name}\'s albums:')
    for num, album in enumerate(albums, start=1):
        print(f'{num}: {album[0]}')
    album_num = int(input('Select an album with its number.\n')) - 1
    print(f'You selected: {albums[album_num][0]}')
    album_name = albums[album_num][0]

    songs = get_songs(albums[album_num][1])
    if len(songs) == 1:
        print('1 song found.')
    else:
        print(f'{len(songs)} songs found.')
        print(f'Songs in {album_name}:')
    for num, song in enumerate(songs, start=1):
        min, sec = divmod(song[2] // 1000, 60)
        print(f'{num}: {song[0]} ({min}:{sec:02d})')
    song_num = int(input('Select a song with its number.\n')) - 1
    print(f'You selected: {songs[song_num][0]}')
    

if __name__ == '__main__':
    main()