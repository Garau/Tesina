import backend.utils.db as utils
import urllib.request
import json
import os
import xmltodict

from pathlib import Path

from flask import render_template
from flask import redirect

def search(request, session, key=None):
	if key != None:
		
		key = key.replace(' ', '%20')
		url_albums = "https://itunes.apple.com/search?term={}&media=music&entity=album&country=IT&limit=20".format(key)
		result_albums = urllib.request.urlopen(url_albums)
		result_albums = json.loads(result_albums.read())['results']

		album_names = []
		album_paths = []

		for results in result_albums:
			album_names.append(results['collectionName'])
			path = r"static/covers/" + results['artistName'] + "_" + results['collectionName'] + ".jpg"
			if os.path.isfile(path):
				path = "../" + path
				album_paths.append({'path': path, 'name': results['collectionName'], 'artist': results['artistName']})
			else:
				album_paths.append({'path': results['artworkUrl100'], 'name': results['collectionName'], 'artist': results['artistName']})

		return render_template("search.html", dict_albums = album_paths)
	else:
		print ("Key is none")
		key = request.form.get('search_key')
		return redirect("search/" + key)

'''
		db =  utils.pysqlite3()
		query_albums = """
				SELECT nome, nome_artista
				FROM album
				WHERE nome LIKE '%{}%'
				ORDER BY nome
				""".format(key)

		query_artists = """
				SELECT nome, genere
				FROM artista
				WHERE nome LIKE '%{}%'
				GROUP BY nome
				ORDER BY nome
				""".format(key)

		result_albums = db.query_db(query_albums)
		result_artists = db.query_db(query_artists)

		if result_artists != None:
			dict_artists = []
			for artists in result_artists:
				dict_artists.append({'artist': artists[0], 'genre': artists[1], 'valid': True})

		if result_albums != None:
			dict_albums = []
			for albums in result_albums:
				dict_albums.append({'name': albums[0], 'artist': albums[1], 'valid': True})

			if result_artists != None:
				return render_template("search.html", dict_artists = dict_artists, dict_albums = dict_albums)
			else:
				return render_template("search.html", dict_albums = dict_albums)
		else:
			return render_template("search.html", error = True)



		url_artist = "https://itunes.apple.com/search?term={}&media=music&entity=musicArtist&country=IT&limit=20".format(key)
		result_artists = urllib.request.urlopen(url_artist)
		result_artists = json.loads(result_artists.read())['results']

		url_artist = "http://ws.audioscrobbler.com/2.0/?method=artist.search&country=porcodio&artist={}&limit=4&api_key=6be54ea8ecd35448b04f9d29183d0138&format=json".format(key)
		result = urllib.request.urlopen(url_artist)
		json_dict = json.loads(result.read())
		result_artists = json_dict['results']['artistmatches']['artist']

		#xml_dict['lfm']['results']['artistmatches']['artist'][1].keys()
		dict_artists = []

		for n in range (0, len(result_artists)):
			artist_name = result_artists[n]['name']
			path = r"static/artists/" + artist_name + ".jpg"
			if os.path.isfile(path):
				path = "../" + path
				dict_artists.append({'path': path, 'name': artist_name})
			else:
				path = result_artists[n]['image'][2]['#text']
				if not path:
					path = "../static/not_found.png"
				dict_artists.append({'path': path, 'name': artist_name})
				'''