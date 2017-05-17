import itunespy

import sqlite3

conn = sqlite3.connect('data/db.db')
c = conn.cursor()

artist_name = "Radiohead"

artist = itunespy.search_artist(artist_name)
albums = []

for item in artist:
	albums += item.get_albums()

for albums in albums:
	name = albums.collection_name
	genre = albums.primary_genre_name
	date = albums.release_date[0:10]
	c.execute('INSERT INTO album VALUES (NULL, ?, ?, ?, NULL, ?) ', (name, genre, artist_name, date))
	conn.commit()