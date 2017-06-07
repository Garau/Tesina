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
		url_albums = "https://itunes.apple.com/search?term={}&media=music&entity=album&country=US&limit=20".format(key)
		result_albums = urllib.request.urlopen(url_albums)
		result_albums = json.loads(result_albums.read())['results']

		album_names = []
		album_paths = []

		for results in result_albums:
			album_names.append(results['collectionName'])
			album_paths.append({'path': results['artworkUrl100'], 'name': results['collectionName'], 'artist': results['artistName']})

		return render_template("search.html", dict_albums = album_paths)
	else:
		print ("Key is none")
		key = request.form.get('search_key')
		return redirect("search/" + key)