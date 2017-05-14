import sqlite3

from flask import Flask
from flask import render_template
from flask import session
from flask import request


from backend.home import home
from backend.signup import signup
from backend.login import login
from backend.logout import logout

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

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/genres')
def genres():
    return render_template('genres.html')

@app.route('/profile')
def profile():
	return render_template('profile.html')

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