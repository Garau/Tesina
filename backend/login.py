import itunespy
import backend.utils.db as utils

from flask import render_template

def login(request, session):
	if 'username' not in request.form:
		return render_template('login.html', flag = False)
	else:
		username = request.form['username']
		query = """
				SELECT psw, id_utente
				FROM utente
				WHERE utente.username = '%s'
				""" % (username)
		db =  utils.pysqlite3()
		result = db.query_db(query)
		psw = result[0][0]

		if(psw == request.form['password']):
			session['username'] = username
			session['user_id'] = result[0][1]
			return render_template('login.html', flag = True, username = username)
		else:
			print("password errata")