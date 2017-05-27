import itunespy
import sqlite3
import urllib.request

conn = sqlite3.connect('data/db.db')
c = conn.cursor()

artist_name = "Green day"

''''''

#artist info

artist_url = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={}&api_key=6be54ea8ecd35448b04f9d29183d0138".format(artist_name)
xml = urllib.request.urlopen(artist_url)

xml_dict = xmltodict.parse(xml)
img_url = xml_dict['lfm']['artist']['image'][3]['#text']
artist_name = xml_dict['lfm']['artist']['name']

urllib.request.urlretrieve(img_url, "static/artists/" + artist_name  + ".png")

''''''

artist = itunespy.search_artist(artist_name)
albums = []

for item in artist:
	albums += item.get_albums()

for albums in albums:
	name = albums.collection_name
	genre = albums.primary_genre_name
	date = albums.release_date[0:10]
	url = albums.artwork_url_100
	url_big = url.replace("100", "600")

	ret = urllib.request.urlopen(url)
	ret2 = urllib.request.urlopen(url_big)

	if ret.code == 200 and ret2.code == 200:
		urllib.request.urlretrieve(url, "static/covers/" + artist_name + "_" + name + ".jpg")
		urllib.request.urlretrieve(url_big, "static/covers/big/" + artist_name + "_" + name + ".jpg")
		c.execute('INSERT INTO album VALUES (NULL, ?, ?, ?, NULL, ?) ', (name, genre, artist_name, date))
		conn.commit()