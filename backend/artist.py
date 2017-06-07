import urllib.request
import xmltodict
import json
import backend.utils.db as utils
import backend.utils.get_links as links
import os

from pathlib import Path

from flask import render_template
from flask import redirect

API_KEY = "6be54ea8ecd35448b04f9d29183d0138"

def artist(request, session, artist_name = None, album_name = None):
	artist_name = artist_name.title()

	if album_name is None: 
		artist_xml = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={}&api_key={}".format(artist_name, API_KEY)
		xml = urllib.request.urlopen(artist_xml)
		xml_dict = xmltodict.parse(xml)
		
		#print (xml_dict['lfm']['artist']['bio'].keys())
		artist_info = xml_dict['lfm']['artist']['bio']['summary']

		if artist_info is None:
			artist_info = "Nessuna descrizione disponibile"

		try:
			artist_path = xml_dict['lfm']['artist']['image'][3]['#text']
		except:
			artist_path = "../static/not_found.jpg"

		artist_info = artist_info.split('<a', 1)[0]
		top_albums = get_top_albums(artist_name, API_KEY)

		return render_template("artist.html", artist_name = artist_name, artist_info = artist_info, 
			artist_path = artist_path, top_albums = top_albums)
	else:
		artist_name = artist_name.replace("/","_")
		album_name = album_name.replace("/", "_")
		artist_name = artist_name.replace(" ","%20")
		album_name = album_name.replace(" ", "%20")

		url_album = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={}&artist={}&album={}&format=json".format(API_KEY, artist_name, album_name)

		json_album = urllib.request.urlopen(url_album)
		json_album = json.loads(json_album.read())

		try:
			album_info = json_album['album']['wiki']['summary']
		except:
			album_info = "No description available"

		album_info = album_info.split('<a', 1)[0]

		album_path = links.get_album_art(album_name)

		songs = links.get_tracklist(album_name)

		#top_albums = get_top_albums(artist_name, API_KEY)
		#return render_template("album.html", artist_name = artist_name, album_name = album_name, album_path=album_path, album_info = album_info, songs = songs, top_albums = top_albums)
		return render_template("album.html", artist_name = artist_name, album_name = album_name, album_path=album_path, album_info = album_info, songs = songs)

def get_top_albums(artist_name, API_KEY):
	top_album_xml = "http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={}&api_key={}".format(artist_name, API_KEY)
	xml_top_album = urllib.request.urlopen(top_album_xml)
	xml_dict_top = xmltodict.parse(xml_top_album)

	top_albums = []

	for i in range(0,4):
		try:
			img_url = xml_dict_top['lfm']['topalbums']['album'][i]['image'][3]['#text']
			album_name = xml_dict_top['lfm']['topalbums']['album'][i]['name']
			top_albums.append({'path': img_url, 'name': album_name, 'artist': artist_name})
		except:
			print ("path not found in album")

	return top_albums