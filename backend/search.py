import backend.utils.db as utils

from flask import render_template
from flask import redirect

def search(request, session, key=None):
	if key != None:
		db =  utils.pysqlite3()
		query = """
				SELECT nome, nome_artista
				FROM album
				WHERE nome LIKE '%{}%'
				""".format(key)
		result = db.query_db(query)

		if result != None:
			dict_albums = []
			for albums in result:
				dict_albums.append({'name': albums[0], 'artist': albums[1]})
			return render_template("search.html", dict_albums = dict_albums)
		else:
			return render_template("search.html", error = True)
	else:
		print ("Key is none")
		key = request.form.get('search_key')
		return redirect("search/" + key)