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

	query = """SELECT recensione.titolo, recensione.testo, recensione.voto, recensione.id_recensione
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
	review_id = result[0][3]

	if 'content' in request.form:
		query = """
		INSERT INTO commento
		VALUES (NULL, '{}', {}, {})
		""".format(request.form['content'], review_id, session['user_id'])
		db.query_db(query)

	query = """SELECT AVG(recensione.voto)
		FROM album, recensione
		WHERE album.id_album = recensione.id_album
		AND album.id_itunes = {}
		GROUP BY recensione.id_album
		ORDER BY AVG(recensione.voto) DESC
	""".format(album_id)
	result = db.query_db(query)
	rating = result[0][0]

	comments = get_comments(album_id)

	return render_template('view_review.html', username=username, artist_name=artist_name, album_name=album_name, album_id = album_id, album_path=album_path, rating = rating, title = title, content = content, user_rating = user_rating, comments = comments)

def get_comments(id_itunes):
	comments = []
	'''
	query = """
	SELECT inn.testo, inn.id_utente, utente.immagine, utente.username
	FROM(
	SELECT commento.id_commento, commento.testo, commento.id_utente
	FROM commento, recensione, utente
	WHERE commento.id_recensione = recensione.id_recensione
	AND recensione.id_utente = utente.id_utente
	AND utente.username = '{}'
	) as inn, utente
	WHERE utente.id_utente = inn.id_utente
	""".format(username)'''
	query = """
	SELECT inn.testo, inn.id_utente, utente.immagine, utente.username
	FROM(
	SELECT commento.id_commento, commento.testo, commento.id_utente
	FROM commento, recensione, utente, album
	WHERE commento.id_recensione = recensione.id_recensione
	AND recensione.id_utente = utente.id_utente
	AND recensione.id_album = album.id_album
	AND album.id_itunes = {}
	) as inn, utente
	WHERE utente.id_utente = inn.id_utente
	""".format(id_itunes)

	result = db.query_db(query)
	if result:
		for line in result:
			comments.append({'text': line[0], 'profile_pic': line[2], 'author': line[3]})
	else:
		comments= None

	return comments