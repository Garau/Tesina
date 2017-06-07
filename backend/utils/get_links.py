import json
import urllib.request

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

def lookup_covers(dict):
	path = "https://itunes.apple.com/lookup?id="
	ids = ""

	for albums in dict:
		ids = ids + str(albums['id_itunes']) + ","

	ids = ids[:-1]


	path = path + ids + "&entity=album&limit=1"
	result_albums = urllib.request.urlopen(path)
	link = json.loads(result_albums.read())['results']

	path_dict = []

	for item in link:
		path_dict.append({'path': item['artworkUrl100'].replace("100", "600")})

	return path_dict

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
'''
API_KEY = "6be54ea8ecd35448b04f9d29183d0138"
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