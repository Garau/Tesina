import urllib.request
import xmltodict
import json
import datetime
import backend.utils.db as utils
import backend.utils.get_links as links

from flask import render_template
from flask import redirect
from flask import url_for

db =  utils.pysqlite3()

def view_review(request, session, username, artist_name, album_name, album_id):
	album_path = links.lookup_cover(album_id)

	query = """SELECT recensione.titolo, recensione.testo, recensione.voto
			FROM album, recensione, utente
			WHERE album.id_album = recensione.id_album
			AND recensione.id_utente = utente.id_utente
			AND album.id_itunes = {}
			AND utente.username = '{}'
			GROUP BY recensione.id_album
			ORDER BY AVG(recensione.voto) DESC
			""".format(album_id, username)
	result = db.query_db(query)
	title = result[0][0]
	content = result[0][1]
	user_rating = result[0][2]

	query = """SELECT AVG(recensione.voto)
		FROM album, recensione
		WHERE album.id_album = recensione.id_album
		AND album.id_itunes = {}
		GROUP BY recensione.id_album
		ORDER BY AVG(recensione.voto) DESC
	""".format(album_id)
	result = db.query_db(query)
	rating = result[0][0]

	return render_template('view_review.html', username=username, artist_name=artist_name, album_name=album_name, album_path=album_path, rating = rating, title = title, content = content, user_rating = user_rating)