import json
import urllib.request
import datetime
import xmltodict
import string
import random

from datetime import timedelta
from datetime import datetime
from urllib.parse   import quote
from urllib.request import urlopen

def get_album_art_small(album_name):
	album_name = album_name.replace(" ", "%20")
	url_albums = "https://itunes.apple.com/search?term={}&media=music&entity=album&country=IT&limit=1".format(album_name)
	result_albums = urllib.request.urlopen(url_albums)
	link = json.loads(result_albums.read())['results'][0]['artworkUrl100']
	return link

def get_album_art(album_name):
	album_name = album_name.replace(" ", "%20")
	url_albums = "https://itunes.apple.com/search?term={}&media=music&entity=album&country=IT&limit=1".format(album_name)
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


	path = path + ids + "&entity=album&limit=1&country=IT"
	result_albums = urllib.request.urlopen(path)
	link = json.loads(result_albums.read())['results']

	path_dict = []

	for item in link:
		path_dict.append({'path': item['artworkUrl100'].replace("100", "600"), 'id': item['collectionId']})

	return path_dict

def lookup_cover(id_itunes):
	#url_albums = "https://itunes.apple.com/lookup?id={}&country=IT&format=json".format(id_itunes)
	url_albums = "https://itunes.apple.com/lookup?id={}&format=json&country=IT".format(id_itunes)
	result_albums = urllib.request.urlopen(url_albums)
	result_albums = json.loads(result_albums.read())

	return result_albums['results'][0]['artworkUrl100'].replace("100", "600")

def lookup_info(id_itunes):
	url_albums = "https://itunes.apple.com/lookup?id={}&country=IT&format=json".format(id_itunes)
	result_albums = urllib.request.urlopen(url_albums)
	result_albums = json.loads(result_albums.read())

	print(result_albums['results'][0].keys())
	info = []
	image = result_albums['results'][0]['artworkUrl100'].replace("100", "600")
	date = result_albums['results'][0]['releaseDate']
	genre = result_albums['results'][0]['primaryGenreName']
	price = result_albums['results'][0]['collectionPrice']
	url = result_albums['results'][0]['collectionViewUrl']
	info.append({'image': image, 'date': date, 'genre': genre, 'price': price, 'url': url})

	return info

def get_tracklist(album_name):
	album_name = album_name.replace(" ", "%20")
	album_name = album_name.encode('utf-8')

	url_albums = "https://itunes.apple.com/search?term={}&media=music&entity=album&country=IT&limit=1".format(album_name)
	result_albums = urllib.request.urlopen(url_albums)
	id_itunes = json.loads(result_albums.read())['results'][0]['collectionId']

	songs_url = "https://itunes.apple.com/lookup?id={}&entity=song".format(id_itunes)

	songs = urllib.request.urlopen(songs_url)
	songs = json.loads(songs.read())

	track_list = []

	for n in range(1, len(songs['results'])):
		track_list.append({"name": songs['results'][n]['trackName']})

	return track_list

def get_tracklist_lookup(albumId):
	songs_url = "https://itunes.apple.com/lookup?id={}&country=IT&entity=song".format(albumId)

	songs = urllib.request.urlopen(songs_url)
	songs = json.loads(songs.read())

	track_list = []

	for n in range(1, len(songs['results'])):
		track_list.append({"name": songs['results'][n]['trackName']})

	return track_list

def get_new_albums(num):
	url = "https://rss.itunes.apple.com/api/v1/it/itunes-music/new-music/{}/explicit/json".format(num)
	result = urllib.request.urlopen(url)
	result = json.loads(result.read())

	albums = []

	for album in result['feed']['results']:
		path = album['artworkUrl100'].replace('100', '600')
		albums.append({'name': album['name'], 'artist': album['artistName'], 'path': path, 'id': album['id']})

	return albums

def return_ago(date):
	dt1 = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
	dt2 = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")

	delta = dt2 - dt1

	seconds  = delta.seconds
	minutes = int(delta.seconds/60)
	hours = int(minutes/60)
	days = delta.days

	if days == 0:
		if hours == 0:
			if minutes == 0:
				final = str(seconds) + "s fa"
			else:
				final = str(minutes) + "m " + str((seconds - minutes*60)) + "s fa"
		else:
			final = str(hours) + "h " + str(minutes-hours*60) + "m fa"
	else:
		if days == 1:
			final = str(days) + " giorno fa"
		else:
			final = str(days) + " giorni fa"

	return final

def get_mbid(artist_name, album_name1, album_name2):
	mbid = None
	if album_name1 and album_name2:
		album_name1 = quote(album_name1.split(' ', 1)[0])
		album_name2 = quote(album_name2.split(' ', 1)[0])
		#artist_name = artist_name.encode('utf-16').decode("utf-8") 
		artist_name = quote(artist_name)

		url = "http://musicbrainz.org/ws/2/recording/?query=release:%22{}%22%20OR%20release:%22{}%22%20AND%20artist:%22{}%22&limit=1".format(album_name1.replace(" ", "%20"), album_name2.replace(" ", "%20"), artist_name.replace(" ", "%20"))
		result = urllib.request.urlopen(url)
		result = xmltodict.parse(result)

		try:
			mbid = result['metadata']['recording-list']['recording']['artist-credit']['name-credit']['artist']['@id']
		except:
			mbid = ""

	return mbid

def get_songs(key):
	url_songs = "https://itunes.apple.com/search?term={}&entity=song&attribute=songTerm&country=IT&limit=10".format(key.replace(" ", "%20"))
	result_songs = urllib.request.urlopen(url_songs)
	result_songs = json.loads(result_songs.read())

	songs = []

	for n in range(result_songs['resultCount']):
		image = result_songs['results'][n]['artworkUrl30'].replace("30", "200")
		songs.append({'trackName': result_songs['results'][n]['trackName'], 'artistName': result_songs['results'][n]['artistName'],
		'artistId': result_songs['results'][n]['artistId'], 'collectionName': result_songs['results'][n]['collectionName'],
		'collectionId': result_songs['results'][n]['collectionId'], 'releaseDate': result_songs['results'][n]['releaseDate'],
		'genre': result_songs['results'][n]['primaryGenreName'], 'prize': result_songs['results'][n]['trackPrice'], 'image': image, })

	return songs

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
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

url_album = "http://ws.audioscrobbler.com/2.0/?method=artist.search&artist={}&api_key={}&format=json".format(artist_name, API_KEY)

json_album = urllib.request.urlopen(url_album)
json_album = json.loads(json_album.read())

print (json_album['results']['artistmatches']['artist'][0].keys())

for artist in json_album['results']['artistmatches']['artist']:
	print (artist['name'])
'''
'''
#Search for artists by given name
artist_name = "Buckethead"
artist_name = artist_name.replace(' ', '%20')
url_albums = "https://itunes.apple.com/search?term={}&media=music&entity=musicArtist&country=US&limit=10".format(artist_name)
result_albums = urllib.request.urlopen(url_albums)
result_albums = json.loads(result_albums.read())['results']

print (result_albums[0].keys())

for n in range(0, len(result_albums)):
	print (result_albums[n]['artistName'])
	print (result_albums[n]['artistLinkUrl'])
	print (result_albums[n]['artistId'])
	print (result_albums[n]['artistType'])
'''
'''
url_albums = "https://itunes.apple.com/lookup?id=81938625&entity=album"
result_albums = urllib.request.urlopen(url_albums)
result_albums = json.loads(result_albums.read())

print (result_albums['results'][1])

#print ("taylor: http://is3.mzstatic.com/image/thumb/Music7/v4/68/68/41/68684190-833b-bfb4-5018-e5a2e6f69eb0/source/10000x10000-999.jpg")
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
key = "buckethead"

url_artists = "http://ws.audioscrobbler.com/2.0/?method=artist.search&artist={}&api_key=6be54ea8ecd35448b04f9d29183d0138&limit=20&format=json".format(key)

result_artists = urllib.request.urlopen(url_artists)
result_artists = json.loads(result_artists.read())

artists = []

for artist in result_artists['results']['artistmatches']['artist']:
	artists.append({'name': artist['name'], 'path': artist['image'][2]['#text']})
'''

'''
url_artists = "https://itunes.apple.com/lookup?id=426856235&entity=album&limit=1"
result_artists = urllib.request.urlopen(url_artists)
result_artists = json.loads(result_artists.read())

print (result_artists)

for n in range (1, len(result_artists['results'])):
	print (result_artists['results'][n]['collectionName'])
'''
'''
album_name="Com"
artist_name = "Radiohead"

album_name = album_name.split(' ', 1)[0]
url = "http://musicbrainz.org/ws/2/recording/?query=release:%22{}%22%20AND%20artist:%22{}%22&limit=1".format(album_name.replace(" ", "%20"), artist_name.replace(" ", "%20"))
print(url)
print("Artist: " + artist_name + " | album_name: " + album_name)
result = urllib.request.urlopen(url)
result = xmltodict.parse(result)

print(result['metadata']['recording-list']['recording']['artist-credit']['name-credit']['artist']['@id'])
'''

'''
url_artists = "http://itunes.apple.com/WebObjects/MZStoreServices.woa/ws/genres?id=1621&limit=1006"
result_artists = urllib.request.urlopen(url_artists)
result = json.loads(result_artists.read())

print(result['1621']['url'])
'''
'''
url_artists = "https://itunes.apple.com/search?term=Buckethead&entity=album&genreId=1153&limit=10&sort=recent"
result_artists = urllib.request.urlopen(url_artists)
result = json.loads(result_artists.read())

print(result['results'][0].keys())

for line in result['results']:
	print(line['collectionName'] + " | " + line['artistName'])
'''