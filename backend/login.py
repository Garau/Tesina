import itunespy
import backend.utils.db as utils

from flask import render_template

db =  utils.pysqlite3()

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
		try:
			result = db.query_db(query)
			psw = result[0][0]
		except:
			error = "Username errato"
			return render_template('error.html', error = error)

		if(psw == request.form['password']):
			session['username'] = username
			session['user_id'] = result[0][1]
			return render_template('login.html', flag = True, username = username)
		else:
			error = "Password errata"
			return render_template('error.html', error = error)