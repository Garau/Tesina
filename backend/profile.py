import backend.utils.db as utils
import backend.utils.get_links as links

from flask import render_template
from flask import redirect
from flask import url_for

db =  utils.pysqlite3()

def profile(request, session, username = None):

	if 'image' in request.form:
		print("image change")
		path = request.form['image']
		query = """
		UPDATE utente
		SET immagine = '{}'
		WHERE username = '{}'
		COLLATE NOCASE
		""".format(path, username)
		db.query_db(query)
		return redirect(url_for('route_profile', username = session['username']))

	query = """
	SELECT immagine, nome, cognome, email
	FROM utente
	WHERE username = '{}'
	COLLATE NOCASE
	""".format(username)
	result = db.query_db(query)


	profile_pic = result[0][0]
	name = result[0][1]
	surname = result[0][2]
	email = result[0][3]
	review_num = get_review_num(username)
	comment_num = get_comment_num(username)
	fav_genre = get_fav_genre(username)
	fav_albums = get_fav_albums(username)
	
	if username == session['username']:
		return render_template('profile.html', session = True, username = username, profile_pic = profile_pic, name = name, surname = surname, email = email, review_num = review_num, comment_num = comment_num, fav_genre = fav_genre, fav_albums = fav_albums, image = profile_pic)
	else:
		if 'username' not in session:
			print("You are not logged")
			return render_template('profile.html', other = True, username = username, profile_pic = profile_pic, name = name, surname = surname, email = email, review_num = review_num, comment_num = comment_num, fav_genre = fav_genre, fav_albums = fav_albums)
		else:
			print("You are not " + username)
			return render_template('profile.html', session = True, other = True, username = username, profile_pic = profile_pic, name = name, surname = surname, email = email, review_num = review_num, comment_num = comment_num, fav_genre = fav_genre, fav_albums = fav_albums)

def get_review_num(username):
	query = """
	SELECT COUNT(recensione.testo)
	FROM album, recensione, utente
	WHERE album.id_album = recensione.id_album
	AND recensione.id_utente = utente.id_utente
	AND utente.username = '{}'
	""".format(username)
	return db.query_db(query)[0][0]

def get_fav_genre(username):
	query="""
	SELECT MAX(num), genere
	FROM (
		SELECT album.genere, COUNT(album.genere) as num
		FROM album, recensione, utente
		WHERE album.id_album=recensione.id_album
		AND recensione.id_utente=utente.id_utente
		AND utente.username = '{}'
		GROUP BY album.genere
	)
	""".format(username)
	return db.query_db(query)[0][1]

def get_fav_albums(username):
	albums = []
	query = """
	SELECT album.nome, recensione.voto, artista.nome, album.id_itunes
	FROM album, recensione, utente, composizione, artista
	WHERE album.id_album=recensione.id_album
	AND recensione.id_utente=utente.id_utente
	AND album.id_album = composizione.id_album
	AND composizione.id_artista = artista.id_artista
	AND utente.username = '{}'
	ORDER BY recensione.voto DESC
	LIMIT 4
	""".format(username.title())
	result = db.query_db(query)
	for line in result:
		path = links.lookup_cover(line[3])
		albums.append({'name': line[0], 'artist': line[2], 'id_itunes': line[3], 'path': path})
	return albums

def get_comment_num(username):
	query = """
	SELECT COUNT(commento.id_commento)
	FROM utente, commento
	WHERE commento.id_utente = utente.id_utente
	AND utente.username='{}'
	""".format(username)
	result = db.query_db(query)
	return result[0][0]