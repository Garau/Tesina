import urllib.request
import xmltodict
import backend.utils.db as utils
import os

from pathlib import Path

from flask import render_template
from flask import redirect

API_KEY = "6be54ea8ecd35448b04f9d29183d0138"

def artist(request, session, artist_name = None, album_name = None):
	print ("album name - " + album_name)
	if album_name is None: 

		artist_xml = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={}&api_key={}".format(artist_name, API_KEY)
		top_album_xml = "http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={}&api_key={}".format(artist_name, API_KEY)
		
		xml = urllib.request.urlopen(artist_xml)
		xml_top_album = urllib.request.urlopen(top_album_xml)

		xml_dict = xmltodict.parse(xml)
		xml_dict_top = xmltodict.parse(xml_top_album)
		

		artist_info = xml_dict['lfm']['artist']['bio']['content']

		if artist_info is None:
			artist_info = "Nessuna descrizione disponibile"

		top_albums = []


		for i in range(0,4):
			try:
				album_name = xml_dict_top['lfm']['topalbums']['album'][i]['name']
				path = r"static/covers/big/" + artist_name + "_" + album_name + ".jpg"

				if os.path.isfile(path):
					path = "../" + path
					top_albums.append({'path': path, 'name': album_name, 'artist': artist_name})
				else:
					img_url = xml_dict_top['lfm']['topalbums']['album'][i]['image'][3]['#text']
					path = "../" + path
					top_albums.append({'path': img_url, 'name': album_name, 'artist': artist_name})
			except:
				print ()
		artist_path = r"static/artists/" + artist_name + ".jpg"

		if os.path.isfile(artist_path):
			artist_path = "../" + artist_path
		else:
			try:
				artist_path = xml_dict['lfm']['artist']['image'][3]['#text']
			except:
				artist_path = "../static/not_found.jpg"

		return render_template("artist.html", artist_name = artist_name, artist_info = artist_info, 
			artist_path = artist_path, top_albums = top_albums)
	else:
		return render_template("album.html", artist_name = artist_name, album_name = album_name)