import itunespy
import backend.utils.db as utils
import backend.utils.get_links as links
import random

from datetime import timedelta
from datetime import datetime
from random import randint
#randint(0,9)
#db.query_db(query)

from flask import render_template

db =  utils.pysqlite3()

num_albums = db.query_db("SELECT COUNT(id_album) FROM album")[0][0]

def home(request, session):
	

	image = get_top_albums(4)
	image2 = get_latest_reviews(9)
	image3 = links.get_new_albums(9)
	comments = get_latest_comments(9)

	if 'username' not in session:
		return render_template('home.html', image=image, image2 = image2, image3 = image3, comments = comments)
	else:
		if 'rating' in session:
			album_path = session['album_path']
			session.pop('rating', None)
			session.pop('album_path', None)
			session.pop('album_id', None)
			return render_template('home.html', image=image, image2 = image2, image3 = image3, comments = comments, session = True, username = session['username'], album_path = album_path, rating = True)
		else:
			return render_template('home.html', image=image, image2 = image2, image3 = image3, comments = comments, session = True, username = session['username'])

def get_top_albums(num, size = None):
	albums = []
	paths = []
	final = []

	query = """
		SELECT album.nome, artista.nome, AVG(recensione.voto) as media, album.id_itunes
		FROM album, composizione, artista, recensione
		WHERE album.id_album = composizione.id_album
		AND composizione.id_artista = artista.id_artista
		AND album.id_album = recensione.id_album
		GROUP BY recensione.id_album
		ORDER BY AVG(recensione.voto) DESC
		LIMIT {}
	""".format(num)

	result = db.query_db(query)
        
	if size is not None:
		for results in result:
			albums.append({'name': results[0], 'artist': results[1]})
			paths.append({'id_itunes': results[3]})
	else:
		for results in result:
			albums.append({'name': results[0], 'artist': results[1]})
			paths.append({'id_itunes': results[3]})
	paths = links.lookup_covers(paths)

	for n in range(len(albums)):
		final.append({'name': albums[n]['name'], 'artist': albums[n]['artist'], 'path': paths[n]['path'], 'id': paths[n]['id']})

	return final

def get_latest_reviews(num):
	albums = []
	paths = []
	final = []

	query = """
	SELECT album.nome, album.id_itunes, utente.username, artista.nome
	FROM album, recensione, utente, composizione, artista
	WHERE album.id_album = recensione.id_album
	AND recensione.id_utente = utente.id_utente
	AND album.id_album = composizione.id_album
	AND composizione.id_artista = artista.id_artista
	ORDER BY recensione.data DESC
	LIMIT {}
	""".format(num)
	results = db.query_db(query)

	for result in results:
		albums.append({'artist': result[3], 'name': result[0], 'id': result[1], 'author': result[2]})
		paths.append({'id_itunes': result[1]})

	paths = links.lookup_covers(paths)

	for n in range(0, len(albums)):
		final.append({'name': albums[n]['name'], 'artist': albums[n]['artist'], 'path': paths[n]['path'], 'id': paths[n]['id'], 'author': albums[n]['author']})

	return final

def get_latest_comments(num):
	comments = []
	query = """
	SELECT inn.data, inn.nome, inn.username as author, inn.id_itunes, inn.titolo, utente.nome, inn.artista
	FROM(
		SELECT commento.data, album.nome, utente.username, album.id_itunes, recensione.titolo, commento.id_commento, artista.nome as artista
		FROM commento, recensione, album, utente, composizione, artista
		WHERE commento.id_recensione = recensione.id_recensione
		AND recensione.id_album = album.id_album
		AND recensione.id_utente = utente.id_utente
		AND composizione.id_album = album.id_album
		AND composizione.id_artista = artista.id_artista
		GROUP BY commento.id_recensione
		ORDER BY commento.data DESC
		LIMIT {}
	) as inn, utente, commento
	WHERE commento.id_utente = utente.id_utente
	AND commento.id_commento = inn.id_commento
	""".format(num)
	result = db.query_db(query)

	for line in result:
		comments.append({'date': line[0], 'album_name': line[1], 'review_author': line[2], "id": line[3], 'title': line[4], 'author': line[5], 'artist': line[6]})
	
	return comments