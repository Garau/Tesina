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
from backend.genres import genres
from backend.album import album
from backend.confirm_account import confirm_account
from backend.change_pass import change_pass

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

@app.route('/signup/<secret_key>', methods = ['GET', 'POST'])
def route_signup_secret(secret_key):
    return confirm_account(request, session, secret_key)

@app.route('/search', methods = ['GET', 'POST'])
def route_search():
    return search(request, session)

@app.route('/search/<kind>/<key>', methods = ['GET', 'POST'])
def route_search_key(kind, key):
    return search(request, session, kind, key)

@app.route(u'/artist/<artist_name>/<artist_id>', methods = ['GET', 'POST'])
def route_artist_name(artist_name, artist_id):
    return artist(request,session,artist_name, artist_id)

@app.route('/album/<artist_name>/<album_name>/<album_id>', methods = ['GET', 'POST'])
def route_album(artist_name, album_name, album_id):
    return album(request,session,artist_name,album_name,album_id)

@app.route('/review/<artist_name>/<album_name>/<album_id>', methods = ['GET', 'POST'])
def route_review(artist_name, album_name, album_id):
    return review(request,session,artist_name,album_name,album_id)

@app.route('/review/<username>/<artist_name>/<album_name>/<album_id>', methods = ['GET', 'POST'])
def route_view_review(username, artist_name, album_name, album_id):
    return view_review(request,session,username,artist_name,album_name,album_id)

@app.route('/profile/<username>', methods = ['GET', 'POST'])
def route_profile(username):
    return profile(request, session, username)

@app.route('/profile/<username>/password', methods = ['GET', 'POST'])
def route_change_pass(username):
    return change_pass(request, session, username)

@app.route('/profile', methods = ['GET', 'POST'])
def route_profile_not_user():
    if 'username' in session:
        return redirect(url_for('route_profile', username = session['username']))
    else:
        msg = "Devi accedere prima di visualizzare il tuo profilo!"
        #return redirect(url_for('route_login', msg = True))
        return render_template('login.html', msg = msg, flag = False)

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/genres')
def route_genres():
    return genres(request, session)

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