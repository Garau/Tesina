import backend.utils.db as utils
import urllib.request
import json
import os
import xmltodict

import backend.utils.get_links as links

from pathlib import Path

from flask import render_template
from flask import redirect

API_KEY = "6be54ea8ecd35448b04f9d29183d0138"

def search(request, session, kind = None, key=None):
	songs = None
	results = None

	if key != None:
		if kind == 'artist':
			#ricerca di artisti
			artists = []
			ids = []
			names = []

			key = key.replace(' ', '%20')
			url_artists = "https://itunes.apple.com/search?term={}&media=music&entity=musicArtist&country=IT&limit=10".format(key)
			result_artists = urllib.request.urlopen(url_artists)
			result_artists = json.loads(result_artists.read())['results']


			for n in range(0, len(result_artists)):
				try:
					if result_artists[n]['artistName'] not in names:
						artists.append({'artist': result_artists[n]['artistName'], 'genre': result_artists[n]['primaryGenreName'], 'id': result_artists[n]['artistId']})
						ids.append(result_artists[n]['artistId'])
						names.append(result_artists[n]['artistName'])
				except:
					print("artist not valid")

			songs = get_famous_songs(ids, names)
			'''
			songs = []
			for n in range(len(artists)):
				songs.append(get_songs(artists[n]['artist'], artists[n]['id']))
			'''
			results = artists
			kind = 'artist'

		elif kind == 'song':
			songs = links.get_songs(key)
			results = songs
		else:
			#ricerca di album
			key = key.replace(' ', '%20')
			url_albums = "https://itunes.apple.com/search?term={}&media=music&entity=album&attribute=albumTerm&country=IT&limit=20".format(key)
			result_albums = urllib.request.urlopen(url_albums)
			result_albums = json.loads(result_albums.read())['results']

			album_names = []
			album_paths = []

			for results in result_albums:
				album_names.append(results['collectionName'])
				album_paths.append({'path': results['artworkUrl100'], 'name': results['collectionName'], 'artist': results['artistName'], 'id': results['collectionId']})
			results = album_paths
			kind = 'album'
		return render_template("search.html", dict_results = results, kind = kind, songs = songs)
	else:
		key = request.form.get('search_key')
		kind = request.form.get('kind')
		if kind is None:
			kind = 'albums'
			if key is None:
				return render_template("search.html")
		elif kind == 'Artista':
			kind = 'artist'
		elif kind == 'Album':
			kind = 'album'
		elif kind == 'Canzone':
			kind = 'song' 
		return redirect("search/" + kind + "/" + key)


def has_info(mbid):
	artist_json = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&mbid={}&api_key={}&format=json".format(mbid, API_KEY)
	json_info = urllib.request.urlopen(artist_json)
	info_dict = json.loads(json_info.read())

	try:
		artist_info = info_dict['artist']['bio']['summary']
	except:
		artist_info = None

	if artist_info is None:
		return False
	else:
		return True

def get_famous_songs(ids_list, names):
	url = "https://itunes.apple.com/lookup?id="
	ids = ""

	for n in range(0, len(ids_list)):
		ids = ids + str(ids_list[n]) + ","

	ids = ids[:-1]

	url = url + ids + "&entity=song&limit=5&country=IT"

	songs = []

	result_songs = urllib.request.urlopen(url)
	result_songs = json.loads(result_songs.read())['results']

	n=1
	count = 0

	while n < len(result_songs):
		#songs.append([result_songs[n]['trackName'], result_songs[n+1]['trackName'], result_songs[n+2]['trackName'], result_songs[n+3]['trackName'], result_songs[n+4]['trackName']])
		try:
			song1 = result_songs[n]['trackName']
		except:
			song1 = None

		try:
			song2 = result_songs[n+1]['trackName']
		except:
			song2 = None

		try:
			song3 = result_songs[n+2]['trackName']
		except:
			song3 = None

		try:
			song4 = result_songs[n+3]['trackName']
		except:
			song4 = None

		try:
			song5 = result_songs[n+4]['trackName']
		except:
			song5 = None
		songs.append([song1, song2, song3, song4, song5])

		n=n+6
		count = count + 1
	return songs

def get_songs(artist_name, artist_id):
	url = "https://itunes.apple.com/lookup?id={}&entity=song&limit=5&country=IT".format(artist_id)
	result_songs = urllib.request.urlopen(url)
	result_songs = json.loads(result_songs.read())['results']
	try:
		song1 = result_songs[1]['trackName']
	except:
		song1 = None

	try:
		song2 = result_songs[2]['trackName']
	except:
		song2 = None

	try:
		song3 = result_songs[3]['trackName']
	except:
		song3 = None

	try:
		song4 = result_songs[4]['trackName']
	except:
		song4 = None

	try:
		song5 = result_songs[5]['trackName']
	except:
		song5 = None
	songs = [song1, song2, song3, song4, song5]

	return songs