
import backend.utils.db as utils

from flask import render_template

db =  utils.pysqlite3()

def confirm_account(request, session, key):
	query = """
	SELECT id_utente
	FROM conferma
	WHERE chiave = '{}'
	""".format(key)

	result = db.query_db(query)

	user_id = result[0][0]

	query = """
	UPDATE utente
	SET attivo = 1
	WHERE id_utente = {};
	""".format(user_id)
	db.query_db(query)

	return render_template("login.html", confirm_profile = True, flag = False)