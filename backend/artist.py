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

def artist(request, session, artist_name = None, album_name = None, album_id = None):
	artist_name = artist_name.title()

	if album_name is None: 
		artist_json = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={}&api_key={}&format=json".format(artist_name.replace(" ", "%20"), API_KEY)
		json_info = urllib.request.urlopen(artist_json)
		info_dict = json.loads(json_info.read())

		try:
			artist_info = info_dict['artist']['bio']['summary']
		except:
			artist_info = None

		if artist_info is None:
			artist_info = "Nessuna descrizione disponibile"

		try:
			artist_path = info_dict['artist']['image'][3]['#text']
		except:
			artist_path = "../static/not_found.jpg"

		artist_info = artist_info.split('<a', 1)[0]
		top_albums = get_top_albums(artist_name, API_KEY)

		return render_template("artist.html", artist_name = artist_name, artist_info = artist_info, 
			artist_path = artist_path, top_albums = top_albums)
	else:
		reviews = []
		db =  utils.pysqlite3()
		query = """SELECT AVG(recensione.voto), COUNT (recensione.id_album)
		FROM album, recensione
		WHERE album.id_album = recensione.id_album
		AND album.id_itunes = {}
		GROUP BY recensione.id_album
		ORDER BY AVG(recensione.voto) DESC""".format(album_id)
		result = db.query_db(query)

		if result:
			rating = result[0][0]
			query = """SELECT utente.username, utente.immagine, recensione.titolo, recensione.voto
			FROM recensione, album, utente
			WHERE album.id_album = recensione.id_album
			AND recensione.id_utente = utente.id_utente
			AND album.id_itunes = {}""".format(album_id)
			results = db.query_db(query)

			for result in results:
				reviews.append({'author': result[0], 'profile_pic': result[1],'title': result[2], 'rate': result[3]})
		else:
			rating = None

		artist_name_form = artist_name.replace("/","_")
		album_name_form = album_name.replace("/", "_")
		artist_name_form = artist_name.replace(" ","%20")
		album_name_form = album_name.replace(" ", "%20")

		url_album = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={}&artist={}&album={}&format=json&lang=IT".format(API_KEY, artist_name_form, album_name_form)

		try:
			json_album = urllib.request.urlopen(url_album)
			json_album = json.loads(json_album.read())

			album_info = json_album['album']['wiki']['summary']
		except:
			album_info = "No description available"

		album_info = album_info.split('<a', 1)[0]

		info = links.lookup_info(album_id)
		album_path = info[0]['image']
		releaseDate = info[0]['date'][0:4]
		genre = info[0]['genre']
		price = info[0]['price']
		#album_path = links.lookup_cover(album_id)

		songs = links.get_tracklist(album_name)

		return render_template("album.html", artist_name = artist_name, album_name = album_name, album_path=album_path, album_info = album_info, songs = songs, album_id = album_id, rating = rating, reviews = reviews, releaseDate = releaseDate, genre = genre, price = price)

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