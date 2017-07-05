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
				SELECT psw, id_utente, attivo
				FROM utente
				WHERE utente.username = '%s'
				COLLATE NOCASE
				""" % (username)
		try:
			result = db.query_db(query)
			psw = result[0][0]
		except:
			error = "Username errato"
			return render_template('login.html', flag = False, error = error)

		if result[0][2] == 1:
			if(psw == request.form['password']):
				session['username'] = username
				session['user_id'] = result[0][1]
				return render_template('login.html', flag = True, username = username)
			else:
				error = "Password errata"
				return render_template('login.html', flag = False, error = error)
		else:
			error = "Utente non ancora attivato, controlla la tua email!"
			return render_template('login.html', flag = False, error = error)