import itunespy
import backend.utils.db as utils

from random import randint
#randint(0,9)
#db.query_db(query)

from flask import render_template

def home(request, session):
	num_rec = ['','','','','','','','','']
	image = get_covers()

	if 'username' not in session:
		print(image)
		return render_template('home.html', image=image, num_rec = num_rec)
	else:
		print(image)
		return render_template('home.html', image=image, num_rec = num_rec, session = True, username = session['username'])

def get_covers():

	imm = [None, None, None, None, None, None, None, None, None] #9

	db =  utils.pysqlite3()

	num_albums = db.query_db("SELECT COUNT(id_album) FROM album")[0][0]

	j=0
	while j<9:
		rand = randint(0, num_albums)

		query = "SELECT nome, nome_artista FROM album WHERE album.id_album = '%s'" % (rand)
		result = db.query_db(query)

		artist = itunespy.search_artist(result[0][1])
		albums = artist[0].get_albums()

		i=0
		while albums[i].collection_name != result[0][0]:
			i=i+1
			
		imm[j-1] = albums[i].artwork_url_100.replace('100', '600')
		j=j+1
		print (imm)
	return (imm)