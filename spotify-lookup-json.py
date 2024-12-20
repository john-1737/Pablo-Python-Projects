# Program to learn about JSON requests
# Using Spotify
# Steps:
#    1.  Ask for artist name
#    2.  Get JSON data on album titles / print titles
#    3.  Ask for title of album
#    4.  Get JSON data on song titles / print titles

import requests
import webbrowser
import base64

# Need Spotify ID and Client Secret
# Get these from Spotify Develoer website -- have to create an app first
CLIENT_ID = 'f7db872ce52e4e7291ecdbe0f7ecb74e'
CLIENT_SECRET = '25960c3d4efa40ada5e22ba8b92faa0b'

def get_access_token(client_id, client_secret):
	auth_url = 'https://accounts.spotify.com/api/token'
	auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
	headers = {
		'Authorization': f'Basic {auth_header}',
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	data = {
		'grant_type': 'client_credentials'
	}
	response = requests.post(auth_url, headers=headers, data=data)
	response_data = response.json()
	return response_data['access_token']

def search_artists(artist_name, access_token):
	search_url = 'https://api.spotify.com/v1/search'
	headers = {
		'Authorization': f'Bearer {access_token}'
	}
	params = {
		'q': artist_name,
		'type': 'artist'
	}
	response = requests.get(search_url, headers=headers, params=params)
	data = response.json()
	artists = []
	for artist in data['artists']['items']:
		artists.append([artist['name'],artist['id']])
	return artists

def get_albums(artist_id, access_token):
	albums_url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
	headers = {
		'Authorization': f'Bearer {access_token}'
	}
	response = requests.get(albums_url, headers=headers)
	data = response.json()
	albums = []
	for album in data['items']:
		albums.append([album['name'],album['id']])
	return albums

def get_tracks(album_id, access_token):
	tracks_url = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
	headers = {
		'Authorization': f'Bearer {access_token}'
	}
	response = requests.get(tracks_url, headers=headers)
	data = response.json()
	tracks = []
	print(data['items'][1])
	for song in data['items']:
		tracks.append([song['name'],song['id'],song['duration_ms'],song['external_urls']])
	return tracks

def main():
	access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
	
	artist_name = input("Enter the artist name: ")
	artist_data = search_artists(artist_name, access_token)
	print("Found the following artists")
	for idx , (name, id) in enumerate(artist_data, start=1):
		print(f'{idx}: {name}')
	
	artist_id_input = int(input('\nEnter the number of the artist you want: '))
	print(f'You selected: {artist_data[artist_id_input-1][0]}')
	album_data = get_albums(artist_data[artist_id_input-1][1], access_token)
	print("Found the following albums")
	for idx , (name, id) in enumerate(album_data, start=1):
		print(f'{idx}: {name}')	

	album_id_input = int(input('\nEnter the number of the album you want: '))
	print(f'You selected: {album_data[album_id_input-1][0]}')
	song_data = get_tracks(album_data[album_id_input-1][1], access_token)
	print("That album has the following songs")
	for idx , (name, id, duration, url) in enumerate(song_data, start=1):
		minutes, seconds = divmod(duration // 1000, 60)
		print(f'{idx}: {name}  ({minutes}:{seconds:02d} minutes)')	
	
	yn = input('Would you like to open a song in your browser? (y/n): ')
	if yn == 'y':
		track_input = int(input('Enter the number of the song you want: '))
		print(f'You selected: {song_data[track_input-1][0]}')	
		webbrowser.open(song_data[track_input-1][3]['spotify'])

if __name__ == "__main__":
	main()