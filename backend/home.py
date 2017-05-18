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
	

	image = get_covers_big()
	image2 = get_covers()
	image3 = get_covers_big()
	image4 = get_covers_big()

	print (image)

	if 'username' not in session:
		return render_template('home.html', image=image, image2 = image2, image3 = image3, image4 = image4)
	else:
		return render_template('home.html', image=image, image2 = image2, image3 = image3,  image4 = image4, session = True, username = session['username'])

def get_covers():

	imm = [None, None, None, None, None, None, None, None, None] #9

	rand = []
	rand = random.sample(range(0, num_albums), 9)

	print (rand)

	query = """
			SELECT nome, nome_artista 
			FROM album 
			WHERE album.id_album = '%s' 
			OR album.id_album = '%s' 
			OR album.id_album = '%s' 
			OR album.id_album = '%s'
			OR album.id_album = '%s'
			OR album.id_album = '%s'
			OR album.id_album = '%s'
			OR album.id_album = '%s'
			OR album.id_album = '%s'
			""" % (rand[0], rand[1], rand[2], rand[3], rand[4], rand[5], rand[6], rand[7], rand[8])
	result = db.query_db(query)
	print (result)

	if result != None:
		imm[0]="../static/Covers/" + result[0][1] + "_" + result[0][0] + ".jpg"
		imm[1]="../static/Covers/" + result[1][1] + "_" + result[1][0] + ".jpg"
		imm[2]="../static/Covers/" + result[2][1] + "_" + result[2][0] + ".jpg"
		imm[3]="../static/Covers/" + result[3][1] + "_" + result[3][0] + ".jpg"
		imm[4]="../static/Covers/" + result[4][1] + "_" + result[4][0] + ".jpg"
		imm[5]="../static/Covers/" + result[5][1] + "_" + result[5][0] + ".jpg"
		imm[6]="../static/Covers/" + result[6][1] + "_" + result[6][0] + ".jpg"
		imm[7]="../static/Covers/" + result[7][1] + "_" + result[7][0] + ".jpg"
		imm[8]="../static/Covers/" + result[8][1] + "_" + result[8][0] + ".jpg"

	return (imm)

def get_covers_big():
	imm = [None, None, None, None]

	rand = []
	rand = random.sample(range(0, num_albums), 4)

	print (rand)

	query = "SELECT nome, nome_artista FROM album WHERE album.id_album = '%s' OR album.id_album = '%s' OR album.id_album = '%s' OR album.id_album = '%s'" % (rand[0], rand[1], rand[2], rand[3])
	result = db.query_db(query)
	print (result)

	if result != None:
		imm[0]="../static/Covers/big/" + result[0][1] + "_" + result[0][0] + ".jpg"
		imm[1]="../static/Covers/big/" + result[1][1] + "_" + result[1][0] + ".jpg"
		imm[2]="../static/Covers/big/" + result[2][1] + "_" + result[2][0] + ".jpg"
		imm[3]="../static/Covers/big/" + result[3][1] + "_" + result[3][0] + ".jpg"

	return (imm)