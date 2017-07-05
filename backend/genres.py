#display genre list in a grid: every panel redirect to a search with a genre
'''
Genres:
Pop
Rock
Elettronica
Rap
Alternative
Metal
Jazz
Punk
'''
import backend.utils.db as utils
import backend.utils.get_links as links

from flask import render_template

def genres(request, session):
	genres = []
	genres.append({'name': 'Rock', 'id': 1})
	genres.append({'name': 'Pop', 'id': 2})
	genres.append({'name': 'Alternative', 'id': 3})
	genres.append({'name': 'Rap', 'id': 4})
	genres.append({'name': 'Elettronica', 'id': 5})
	genres.append({'name': 'Metal', 'id': 6})
	genres.append({'name': 'Jazz', 'id': 7})
	genres.append({'name': 'Punk', 'id': 8})
	genres.append({'name': 'Instrumental', 'id': 9})

	return render_template('genres.html', genres = genres)


'''
changelog
aggiunto genres
aggiunto controllo negli insert into per gli apostrofi
agiunto controllo dell'username nella registrazione
aggiunta visualizzazione dell'errore in login
aggiunta funzione "return_ago"
aggiunto tempo passato dall'ultimo commento in forma di stringa

bisogna sistemare query dei commenti (non mostra la recensione, ma i commenti dell'album)
'''

'''
Cosa manca:
1_cambiare impostazioni del profilo
2_aggiungere commenti alle recensione - done
3_ricerca per genere
4_ricerca per artista
5_link per i profili agli autori delle recensioni
'''