import backend.utils.db as utils
import backend.utils.get_links as links

from flask import render_template

db =  utils.pysqlite3()

def change_pass(request, session, username):
	if 'username' in session:
		print("username in session")

		if 'vecchia_password' in request.form:

			print("Cambia password")
			old = request.form['vecchia_password']
			new = request.form['nuova_password']
			confirm_new = request.form['conferma_nuova_password']

			query = "SELECT utente.psw FROM utente WHERE utente.username = '{}' COLLATE NOCASE".format(username)
			psw = db.query_db(query)[0][0]

			if psw == old:
				print("Password corrisponde a quella vecchia")
				if new == confirm_new:
					print("Password nuove corrispondono")
					query = """
					UPDATE utente
					SET psw = '{}'
					WHERE username = '{}'
					COLLATE NOCASE
					""".format(new, username)
					db.query_db(query)
					return render_template('change_pass.html', flag=True, username = username)
				else:
					msg = "Le nuove password non sono le stesse"
					return render_template('change_pass.html', msg = msg, username = username)
			else:
				msg = "Password errata"
				return render_template('change_pass.html', msg = msg, username = username)
		else:
			return render_template('change_pass.html', flag = False, username = username)
	else:
		error = "Devi accedere prima di cambiare la password"
		return render_template('login.html', flag = False, error = error)