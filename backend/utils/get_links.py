import json
import urllib.request
import datetime

def get_album_art_small(album_name):
	album_name = album_name.replace(" ", "%20")
	url_albums = "https://itunes.apple.com/search?term={}&media=music&entity=album&country=US&limit=1".format(album_name)
	result_albums = urllib.request.urlopen(url_albums)
	link = json.loads(result_albums.read())['results'][0]['artworkUrl100']
	return link

def get_album_art(album_name):
	album_name = album_name.replace(" ", "%20")
	url_albums = "https://itunes.apple.com/search?term={}&media=music&entity=album&country=US&limit=1".format(album_name)
	result_albums = urllib.request.urlopen(url_albums)
	link = json.loads(result_albums.read())['results'][0]['artworkUrl100']
	link = link.replace("100", "600")
	return link

def lookup_covers(my_dict):
	path = "https://itunes.apple.com/lookup?id="
	ids = ""

	for albums in my_dict:
		ids = ids + str(albums['id_itunes']) + ","

	ids = ids[:-1]


	path = path + ids + "&entity=album&limit=1"
	result_albums = urllib.request.urlopen(path)
	link = json.loads(result_albums.read())['results']

	path_dict = []

	for item in link:
		path_dict.append({'path': item['artworkUrl100'].replace("100", "600"), 'id': item['collectionId']})

	return path_dict

def lookup_cover(id_itunes):
	url_albums = "https://itunes.apple.com/lookup?id={}&format=json".format(id_itunes)
	result_albums = urllib.request.urlopen(url_albums)
	result_albums = json.loads(result_albums.read())

	return result_albums['results'][0]['artworkUrl100'].replace("100", "600")

def lookup_info(id_itunes):
	url_albums = "https://itunes.apple.com/lookup?id={}&format=json".format(id_itunes)
	result_albums = urllib.request.urlopen(url_albums)
	result_albums = json.loads(result_albums.read())

	info = []
	image = result_albums['results'][0]['artworkUrl100'].replace("100", "600")
	date = result_albums['results'][0]['releaseDate']
	genre = result_albums['results'][0]['primaryGenreName']
	price = result_albums['results'][0]['collectionPrice']
	info.append({'image': image, 'date': date, 'genre': genre, 'price': price})

	return info

def get_tracklist(album_name):
	album_name = album_name.replace(" ", "%20")
	url_albums = "https://itunes.apple.com/search?term={}&media=music&entity=album&country=US&limit=1".format(album_name)
	result_albums = urllib.request.urlopen(url_albums)
	id_itunes = json.loads(result_albums.read())['results'][0]['collectionId']

	songs_url = "https://itunes.apple.com/lookup?id={}&entity=song".format(id_itunes)

	songs = urllib.request.urlopen(songs_url)
	songs = json.loads(songs.read())

	track_list = []

	for n in range(1, len(songs['results'])):
		track_list.append({"name": songs['results'][n]['trackName']})

	return track_list

def get_new_albums(num):
	url = "https://rss.itunes.apple.com/api/v1/us/itunes-music/new-music/{}/explicit/json".format(num)
	result = urllib.request.urlopen(url)
	result = json.loads(result.read())

	albums = []

	for album in result['feed']['results']:
		path = album['artworkUrl100'].replace('100', '600')
		albums.append({'name': album['name'], 'artist': album['artistName'], 'path': path, 'id': album['id']})

	return albums
'''
url_albums = "https://itunes.apple.com/search?term=rust%20in%20piece&media=music&entity=album&country=US&limit=1"
result_albums = urllib.request.urlopen(url_albums)
link = json.loads(result_albums.read())['results'][0]
print (link['collectionId'])
'''

'''
path = "https://itunes.apple.com/lookup?Id="

for ids in paths:
        path = path + ids.id_itunes + ","

path = path + "&entity=music"
'''

API_KEY = "6be54ea8ecd35448b04f9d29183d0138"

'''
artist_name = "pink%20floyd"
album_name = "the%20dark%20side%20of%20the%20moon"

url_album = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={}&artist={}&album={}&format=json".format(API_KEY, artist_name, album_name)
print (url_album)

json_album = urllib.request.urlopen(url_album)
json_album = json.loads(json_album.read())

description = json_album['album']['wiki']['summary']

songs = []

print (json_album['album']['tracks']['track'][0].keys())

for tracks in json_album['album']['tracks']['track']:
	songs.append({'name': tracks['name']})

print (songs)
'''
'''
for tags in json_album['album']['tags']['tag']:
	print (tags['name'])
'''
'''

tag_get_top = "http://ws.audioscrobbler.com/2.0/?method=tag.gettopalbums&tag=guitar virtuoso chillout&api_key=6be54ea8ecd35448b04f9d29183d0138&limit=1&format=json"
json_get_top = urllib.request.urlopen(tag_get_top)
json_get_top = json.loads(json_get_top.read())

print ("Album = " + json_get_top['albums']['album'][0]['name'] + " - Artist = " + json_get_top['albums']['album'][0]['artist']['name'])
'''	
	
'''
album_name = "colma"
url_similar = "https://itunes.apple.com/search?term={}&media=music&entity=album&attribute=albumTerm&country=US&limit=5".format(album_name)

json_similar = urllib.request.urlopen(url_similar)
json_similar = json.loads(json_similar.read())

for albums in json_similar['results']:
	print (albums['artistName'] + " - " + albums['collectionName'])

print (json_similar['results'][0]['primaryGenreName'])
'''
'''
musicgraph api = a2cbfe2a32e66b343eec3d3e3bec2553
artist_name = "buckethead"
album_name = ""

url_similar = "http://api.musicgraph.com/api/v2/album/search?api_key=a2cbfe2a32e66b343eec3d3e3bec2553&similar_to=\'Colma\'&limit=5"

print (url_similar)
json_similar = urllib.request.urlopen(url_similar)
json_similar = json.loads(json_similar.read())

print (json_similar['data'][0].keys())

for items in json_similar['data']:
	print (items['artist_name'] + " - " + items['title'] + " - " + str(items['popularity']))
'''

#DISCOGS - aYYJbJQMVufJyVFneUdswqEkhoecNRFfNzKcIWSi

'''
API_KEY = "6be54ea8ecd35448b04f9d29183d0138"
artist_name = "buckethead"
album_name = "colma"

url_album = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={}&artist={}&album={}&format=json".format(API_KEY, artist_name, album_name)

json_album = urllib.request.urlopen(url_album)
json_album = json.loads(json_album.read())

album_info = json_album['album']['wiki']['summary']

print (album_info)
'''
'''
key = "Siamese Dream"
key = key.replace(' ', '%20')
url_albums = "https://itunes.apple.com/search?term={}&media=music&entity=album&country=US&limit=20".format(key)
result_albums = urllib.request.urlopen(url_albums)
result_albums = json.loads(result_albums.read())['results']

print (result_albums[0].keys())

print (result_albums[0]['artistId'])
print (result_albums[0]['artistName'])

key = result_albums[0]['collectionId']
key = "723539773"
url_albums = "https://itunes.apple.com/lookup?id={}&format=json".format(key)
result_albums = urllib.request.urlopen(url_albums)
result_albums = json.loads(result_albums.read())
#print (result_albums['results'][0].keys())
'''
'''
id_itunes = "288277647"

url_albums = "https://itunes.apple.com/lookup?id={}&format=json".format(id_itunes)
result_albums = urllib.request.urlopen(url_albums)
result_albums = json.loads(result_albums.read())

print (result_albums['results'][0].keys())
name = result_albums['results'][0]['artistName']
genre = result_albums['results'][0]['primaryGenreName']

print (name+ " - " + genre + genre)
'''
#print ("Current date & time " + str(datetime.datetime.now()))
'''
artist_name = "My bloody valentine"

artist_json = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={}&api_key={}&format=json".format(artist_name.replace(" ", "%20"), API_KEY)
print (artist_json)
json_info = urllib.request.urlopen(artist_json)
info_dict = json.loads(json_info.read())

print(info_dict['artist']['bio']['summary'])
'''

'''
Push 14-06-17

Aggiunte tabelle:
_Create Canzone
_Create Appartenenza_lista
_Create Commento
_Add utente(immagine)
Corretta visualizzazione delle informazioni di un artista e della sua immagine
Modificata la grafica:
_album.html (aggiunte le recensioni dei vari utenti sotto il titolo, rimossa descrizione dell'album)
_view_review.html (aggiunta una seconda query)
_home.html (cambiati nomi)

16-06-17
_home.html (aggiunti artista e nome album ai best)
_review.html (aggiunte informazioni all'album, spostate recensioni sotto la tracklist)
_corretto link di redirect a review se non loggati
_aggiunti ultimi album alla home
_tentativi di un carousel sulla home (in backup/tesina_2)
_aggiunti link per jquery, jss e javascript
'''

'''
genre_id = "1621"

url_albums = "http://itunes.apple.com/WebObjects/MZStoreServices.woa/ws/genres?id={}".format(genre_id)
result_albums = urllib.request.urlopen(url_albums)
result_albums = json.loads(result_albums.read())

print ("name: " + result_albums[genre_id]['name'])
print ("name: " + result_albums[genre_id]['url'])

print (result_albums[genre_id].keys())
'''

'''
url = "https://itunes.apple.com/search?term=R+B/Soul&limit=10"
result = urllib.request.urlopen(url)
result = json.loads(result.read())

print (result['results'][0].keys())

for entry in result['results']:
	print (entry['artistName'])
'''
'''
url = "https://rss.itunes.apple.com/api/v1/us/apple-music/new-music/10/explicit/json"
result = urllib.request.urlopen(url)
result = json.loads(result.read())

print (result['feed'].keys())
print ("--------------")
print (result['feed']['results'][0].keys())
'''

'''
Cosa manca:
1_cambiare impostazioni del profilo
2_aggiungere commenti alle recensione
3_ricerca per genere
4_ricerca per artista
'''