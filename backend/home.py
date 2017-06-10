import itunespy
import backend.utils.db as utils
import backend.utils.get_links as links
import random

from random import randint
#randint(0,9)
#db.query_db(query)

from flask import render_template

db =  utils.pysqlite3()

num_albums = db.query_db("SELECT COUNT(id_album) FROM album")[0][0]

def home(request, session):
	

	image = get_top_albums(4)
	image2 = latest_reviews(9)
	image3 = image
	image4 = image

	if 'username' not in session:
		return render_template('home.html', image=image, image2 = image2, image3 = image3, image4 = image4)
	else:
		if 'rating' in session:
			album_path = session['album_path']
			session.pop('rating', None)
			session.pop('album_path', None)
			session.pop('album_id', None)
			return render_template('home.html', image=image, image2 = image2, image3 = image3,  image4 = image4, session = True, username = session['username'], album_path = album_path, rating = True)
		else:
			return render_template('home.html', image=image, image2 = image2, image3 = image3,  image4 = image4, session = True, username = session['username'])

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

def latest_reviews(num):
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
	print (results)

	for result in results:
		albums.append({'artist': result[3], 'name': result[0], 'id': result[1], 'author': result[2]})
		paths.append({'id_itunes': result[1]})

	paths = links.lookup_covers(paths)

	for n in range(0, len(albums)):
		final.append({'name': albums[n]['name'], 'artist': albums[n]['artist'], 'path': paths[n]['path'], 'id': paths[n]['id'], 'author': albums[n]['author']})

	print (final)

	return final