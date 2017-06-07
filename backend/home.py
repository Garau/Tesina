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
	image2 = get_top_albums(4, "small")
	image3 = image
	image4 = image

	if 'username' not in session:
		return render_template('home.html', image=image, image2 = image2, image3 = image3, image4 = image4)
	else:
		return render_template('home.html', image=image, image2 = image2, image3 = image3,  image4 = image4, session = True, username = session['username'])


def get_covers(num, type):
	imm = []
	rand = []

	rand = random.sample(range(0, num_albums), num)

	query = "SELECT nome, nome_artista FROM album WHERE album.id_album = '%s' OR album.id_album = '{}'".format(rand[0])

	for i in range(num-1):
		query = query + " OR album.id_album = '{}'".format(rand[i+1])

	result = db.query_db(query)

	for i in range(num):
		if type == "small":
			path = "../static/Covers/" + result[i][1] + "_" + result[i][0] + ".jpg"
		elif type == "big":
			path = "../static/Covers/big/" + result[i][1] + "_" + result[i][0] + ".jpg"
		imm.append({'path': path, 'artist': result[i][1], 'name': result[i][0]})
	return (imm)


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
		final.append({'name': albums[n]['name'], 'artist': albums[n]['artist'], 'path': paths[n]['path']})

	return final
'''
	Update 31-05-17
rimossi file statici
modificata tabella recensione: aggiunto campo "voto" not null, modificato campo "testo" null, aggiunto check sul voto
modifica tabella album: rimosso campo "nome_artista" perchè era ricavabile dalla tabella "artista"
aggiunti "ON UPDATE CASCADE" alle foreign key
aggiunto campo "path" alla tabella album, per indicare il percorso della cover (troppo lento calcolarlo ogni volta)
iniziata funzione per gli album con voto maggiore

https://gist.github.com/iggym/6023041
https://itunes.apple.com/lookup?id=394123397&entity=album&limit=1 (id = artistId)
'''
