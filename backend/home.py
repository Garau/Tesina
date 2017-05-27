import itunespy
import backend.utils.db as utils
import random

from random import randint
#randint(0,9)
#db.query_db(query)

from flask import render_template

db =  utils.pysqlite3()

num_albums = db.query_db("SELECT COUNT(id_album) FROM album")[0][0]

def home(request, session):
	

	image = get_covers(4, "big")
	image2 = get_covers(9, "small")
	image3 = get_covers(3, "big")
	image4 = get_covers(3, "big")

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