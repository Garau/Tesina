#Application name	Garau reviews
#API key	6be54ea8ecd35448b04f9d29183d0138
#Shared secret	223c73b77f585c52a89308376977f7a6
#Registered to	RaguSheep

#import pylast
import urllib.request
import xmltodict
import json
from pathlib import Path

API_KEY = "6be54ea8ecd35448b04f9d29183d0138"
API_SECRET = "223c73b77f585c52a89308376977f7a6"

username = "RaguSheep"
#password_hash = pylast.md5("crystian1997 ")

xml = urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=emma marrone&api_key=6be54ea8ecd35448b04f9d29183d0138")
xml_top_album = urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist=Buckethead&api_key=6be54ea8ecd35448b04f9d29183d0138")

result = urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method=artist.search&limit=4&artist=biagio%20antonacci&api_key=6be54ea8ecd35448b04f9d29183d0138&format=json")

result_artists = json.loads(result.read())

result_artists = result_artists['results']
print (result_artists['artistmatches']['artist'][1]['name'])

print (result_artists['artistmatches']['artist'][0]['image'][3]['#text'])
print (result_artists['artistmatches']['artist'][1]['image'])
print (result_artists['artistmatches']['artist'][2]['image'][3]['#text'])
print (result_artists['artistmatches']['artist'][3]['image'][3]['#text'])
result_artists['artistmatches']['artist'][1]['image'][3]['#text']
result_artists['artistmatches']['artist'][2]['image'][3]['#text']
result_artists['artistmatches']['artist'][3]['image'][3]['#text']

# xml_dict = xmltodict.parse(xml)
# xml_dict_top_album = xmltodict.parse(xml_top_album)

# print (xml_dict['lfm']['results']['artistmatches']['artist'][1].keys())
# print (len(xml_dict['lfm']['results']['artistmatches']['artist']))

# result_artists = xml_dict['lfm']['results']['artistmatches']['artist']
# print (xml_dict['lfm']['results'].keys())

# print (xml_dict['lfm']['results']['artistmatches']['artist'][1]['mbid'])
# for n in range (0, len(result_artists)):
# 	print (result_artists[n]['name'])
	#print (result_artists[n]['name'][n][3])
# img_url = xml_dict['lfm']['artist']['image'][3]['#text']
# print ( xml_dict['lfm']['artist'].keys())
# print (xml_dict['lfm']['artist'][0])
# artist_name = xml_dict['lfm']['artist']['name']
# print (artist_name)
# artist_info = xml_dict['lfm']['artist']['bio']['content']
# top_album = xml_dict_top_album['lfm']['topalbums']['album'][0]['name']

#print (artist_name)

#urllib.request.urlretrieve(img_url, "static/artists/" + artist_name  + ".png")

''''''
'''
key = "b".replace(' ', '%20')

url = "https://itunes.apple.com/search?term={}&media=music&entity=album&country=IT&limit=20".format(key)
#url = "https://itunes.apple.com/search?term={}&media=music&entity=musicArtist&country=IT&limit=20".format(key)

result = urllib.request.urlopen(url)

json = json.loads(result.read())
num_results = json['resultCount']
result = json['results']
print ("result count = " + str(num_results))
print (result[0].keys())

album_names = []
album_paths = []

for results in result:
	album_names.append(results['collectionName'])
	path = "static/covers/" + results['artistName'] + "_" + results['collectionName'] + ".jpg"
	print (path)
	path = "static/covers/Buckethead_Giant Robot.jpg"
	if Path(path).is_file():
		print ("crissto")
		album_paths.append(path)
	else:
		album_paths.append(results['artworkUrl100'])

#print (result['collectionName'])

print (album_paths)
'''