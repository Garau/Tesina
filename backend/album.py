import urllib.request
import xmltodict
import json
import backend.utils.db as utils
import backend.utils.get_links as links
import os

from pathlib import Path

from flask import render_template
from flask import redirect

def album(request, session, artist_name, album_name, album_id):
	names=[]
	reviews = []
	db =  utils.pysqlite3()
	query = """SELECT AVG(recensione.voto), COUNT (recensione.id_album)
	FROM album, recensione
	WHERE album.id_album = recensione.id_album
	AND album.id_itunes = {}
	GROUP BY recensione.id_album
	ORDER BY AVG(recensione.voto) DESC""".format(album_id)
	result = db.query_db(query)

	if result:
		rating = result[0][0]
		query = """SELECT utente.username, utente.immagine, recensione.titolo, recensione.voto
		FROM recensione, album, utente
		WHERE album.id_album = recensione.id_album
		AND recensione.id_utente = utente.id_utente
		AND album.id_itunes = {}""".format(album_id)
		results = db.query_db(query)

		for result in results:
			names.append(result[0])
			reviews.append({'author': result[0], 'profile_pic': result[1],'title': result[2], 'rate': result[3]})
	else:
		rating = None

	info = links.lookup_info(album_id)
	album_path = info[0]['image']
	releaseDate = info[0]['date'][0:4]
	genre = info[0]['genre']
	price = info[0]['price']
	url = info[0]['url']
	#album_path = links.lookup_cover(album_id)

	songs = links.get_tracklist_lookup(album_id)

	reviewed = False
	if 'username' in session:
		for n in range(len(names)):
			if names[n].lower() == session['username'].lower():
				reviewed = True
				break;

	return render_template("album.html", artist_name = artist_name, album_name = album_name, album_path=album_path, songs = songs, album_id = album_id, rating = rating, reviews = reviews, releaseDate = releaseDate, genre = genre, price = price, url = url, reviewed = reviewed)
