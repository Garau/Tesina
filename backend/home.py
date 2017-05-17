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
	

	image = get_covers()
	image2 = ["ok_computer.jpg", "ok_computer.jpg", "ok_computer.jpg", "ok_computer.jpg", "ok_computer.jpg", "ok_computer.jpg", "ok_computer.jpg", "ok_computer.jpg", "ok_computer.jpg", ]
	image3 = image
	image4 = image

	print (image)

	if 'username' not in session:
		return render_template('home.html', image=image, image2 = image2, image3 = image3, image4 = image4)
	else:
		return render_template('home.html', image=image, image2 = image2, image3 = image3,  image4 = image4, session = True, username = session['username'])

def get_covers():

	imm = [None, None, None, None] #9

	rand = []
	rand = random.sample(range(0, num_albums), 4)

	query = "SELECT nome, nome_artista FROM album WHERE album.id_album = '%s' OR album.id_album = '%s' OR album.id_album = '%s' OR album.id_album = '%s'" % (rand[0], rand[1], rand[2], rand[3])
	result = db.query_db(query)
	print (result)

	if result != None:
		imm[0]="../static/Covers/" + result[0][1] + "_" + result[0][0] + ".jpg"
		imm[1]="../static/Covers/" + result[1][1] + "_" + result[1][0] + ".jpg"
		imm[2]="../static/Covers/" + result[2][1] + "_" + result[2][0] + ".jpg"
		imm[3]="../static/Covers/" + result[3][1] + "_" + result[3][0] + ".jpg"

	return (imm)