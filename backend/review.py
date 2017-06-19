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

def review(request, session, artist_name, album_name, album_id):
	if 'username' not in session:
		return render_template("review.html", artist_name = artist_name, album_name = album_name, album_id = album_id)
	else:
		if 'title' not in request.form:
			query = """SELECT AVG(recensione.voto), album.id_album
			FROM album, recensione
			WHERE album.id_album = recensione.id_album
			AND album.id_itunes = {}
			GROUP BY recensione.id_album
			ORDER BY AVG(recensione.voto) DESC""".format(album_id)
			result = db.query_db(query)

			if result:
				rating = result[0][0]
				session['album_id'] = result[0][1]
			else:
				rating = None

			album_path = links.lookup_cover(album_id)

			return render_template("review.html", artist_name = artist_name, album_path = album_path, album_name = album_name, album_id = album_id, logged = True, rating = rating)
		else:
			print ("do things - insert into")	
			session['rating'] = True
			session['album_path'] = links.lookup_cover(album_id)

			#check if artist exists4

			url_albums = "https://itunes.apple.com/lookup?id={}&format=json".format(album_id)
			result_albums = urllib.request.urlopen(url_albums)
			result_albums = json.loads(result_albums.read())

			artist_id = result_albums['results'][0]['artistId']

			query = """
			SELECT id_artista
			FROM artista
			WHERE id_itunes = {}
			""".format(artist_id)

			result = db.query_db(query)

			if result:
				print ("artist exists")
			else:
				name = result_albums['results'][0]['artistName']
				genre = result_albums['results'][0]['primaryGenreName']

				query = """
				INSERT INTO artista
				VALUES (NULL, '{}','{}',{})
				""".format(name, genre, artist_id)
				try:
					db.query_db(query)
				except:
					error = "Artista già esistente"
					return render_template('error.html', error = error)

			if session.get('album_id'):
				id_album = session['album_id']
			else:
				#insert into album and composizione
				url_albums = "https://itunes.apple.com/lookup?id={}&format=json".format(album_id)
				result_albums = urllib.request.urlopen(url_albums)
				result_albums = json.loads(result_albums.read())

				releaseDate = result_albums['results'][0]['releaseDate'][:10]
				genre = result_albums['results'][0]['primaryGenreName']

				query = "INSERT INTO album VALUES (NULL, '{}', '{}', '{}', {})".format(album_name, genre, releaseDate, album_id)

				print (query)
				db.query_db(query)
				'''
				try:
					db.query_db(query)
				except:
					error = "album già esistente"
					return render_template('error.html', error = error)
				'''
				query = """
				SELECT id_album
				FROM album
				WHERE id_itunes = {}
				""".format(album_id)
				id_album = db.query_db(query)[0][0]

				query = """
				SELECT id_artista
				FROM artista
				WHERE id_itunes = {}
				""".format(artist_id)
				id_artista = db.query_db(query)[0][0]

				query = """
				INSERT INTO composizione
				VALUES ({},{})
				""".format(id_artista, id_album)
				try:
					db.query_db(query)
				except:
					error = "associazione già esistente"
					return render_template('error.html', error = error)

			id_utente = session['user_id']
			titolo = request.form['title']
			testo = request.form['content']
			voto = request.form.get('rating')

			time = datetime.datetime.now()
			query = """
			INSERT INTO recensione
			VALUES (NULL, {},{},'{}','{}',{}, '{}')
			""".format(id_album, id_utente, titolo, testo, voto, time)
			print (query)

			try:
				db.query_db(query)
			except:
				error = "errore nella recensione"
				return render_template('error.html', error = error)

			return redirect(url_for('route_home'))