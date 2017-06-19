import sqlite3

from flask import Flask
from flask import render_template
from flask import session
from flask import request
from flask import redirect
from flask import url_for


from backend.home import home
from backend.signup import signup
from backend.login import login
from backend.logout import logout
from backend.search import search
from backend.artist import artist
from backend.review import review
from backend.view_review import view_review
from backend.profile import profile

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def route_home():
    return home(request, session)
    
@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/login', methods = ['GET', 'POST'])
def route_login():
    return login(request, session)

@app.route('/signup', methods = ['GET','POST'])
def route_signup():
    return signup(request, session)

@app.route('/search', methods = ['GET', 'POST'])
def route_search():
    return search(request, session)

@app.route('/search/<key>', methods = ['GET', 'POST'])
def route_search_key(key):
    return search(request, session, key)

@app.route('/artist', methods = ['GET', 'POST'])
def route_artist():
    return artist(request,session)

@app.route('/artist/<artist_name>', methods = ['GET', 'POST'])
def route_artist_name(artist_name):
    return artist(request,session,artist_name)

@app.route('/artist/<artist_name>/<album_name>/<album_id>', methods = ['GET', 'POST'])
def route_artist_name_album(artist_name, album_name, album_id):
    return artist(request,session,artist_name,album_name,album_id)

@app.route('/review/<artist_name>/<album_name>/<album_id>', methods = ['GET', 'POST'])
def route_review(artist_name, album_name, album_id):
    return review(request,session,artist_name,album_name,album_id)

@app.route('/review/<username>/<artist_name>/<album_name>/<album_id>', methods = ['GET', 'POST'])
def route_view_review(username, artist_name, album_name, album_id):
    return view_review(request,session,username,artist_name,album_name,album_id)

@app.route('/profile/<username>', methods = ['GET', 'POST'])
def route_profile(username):
    return profile(request, session, username)

@app.route('/profile', methods = ['GET', 'POST'])
def route_profile_not_user():
    if 'username' in session:
        return redirect(url_for('route_profile', username = session['username']))
    else:
        return redirect(url_for('route_login'))

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/genres')
def genres():
    return render_template('genres.html')

@app.route('/logout')
def route_logout():
	return logout(request, session)

@app.route('/clear')
def clear():
	session.clear()
	return home(request, session)

app.secret_key = 'chiave%n'

if __name__ == '__main__':
    app.run()