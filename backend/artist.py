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

def artist(request, session, artist_name, artist_id):
	artist_info = "nessuna descrizione disponibile"
	artist_path = "https://pbs.twimg.com/profile_images/600060188872155136/st4Sp6Aw.jpg"
	artist_name = artist_name.title()

	if artist_id:
		top_albums = get_top_albums(artist_id, artist_name)
		print (top_albums)

	if len(top_albums)>0:
		album_name1 = top_albums[0]['name']
		if len(top_albums)>1:
			album_name2 = top_albums[1]['name']

			mbid = links.get_mbid(artist_name, album_name1, album_name2)

			if mbid != "":
				artist_json = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&mbid={}&api_key={}&lang=it&format=json".format(mbid, API_KEY)
				json_info = urllib.request.urlopen(artist_json)
				info_dict = json.loads(json_info.read())
				
				if info_dict['artist']['bio']['summary']:
					artist_info = info_dict['artist']['bio']['summary']
					artist_info = artist_info.split('<a', 1)[0]
					if artist_info == " ":
						artist_info = "Nessuna descrizione disponibile"
				else:
					artist_info = "Nessuna descrizione disponibile"

				if info_dict['artist']['image'][3]['#text']:
					artist_path = info_dict['artist']['image'][3]['#text']
				else:
					artist_path = "nessun path"

		else:
			album_name2 = "nessun album2"
	else:
		album_name1 = "nessun album1"
		album_name2 = "nessun album2"
	
	return render_template("artist.html", artist_name = artist_name, artist_info = artist_info, 
		artist_path = artist_path, top_albums = top_albums)
		
def get_top_albums(artistId, artist_name):
	top_albums = []

	url_artists = "https://itunes.apple.com/lookup?id={}&entity=album&country=IT".format(artistId)
	result_artists = urllib.request.urlopen(url_artists)
	result_artists = json.loads(result_artists.read())

	for n in range (1, len(result_artists['results'])):
		queryId = str(result_artists['results'][n]['artistId'])
		artistId = str(artistId)
		if queryId == artistId:
			top_albums.append({'path': result_artists['results'][n]['artworkUrl100'].replace('100', '600'), 'name': result_artists['results'][n]['collectionName'], 'artist': result_artists['results'][n]['artistName'], 'id': result_artists['results'][n]['collectionId']})

	return top_albums