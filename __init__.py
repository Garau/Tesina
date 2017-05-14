from flask import Flask
from flask import render_template

from backend.home import home

app = Flask(__name__)

@app.route('/')
def route_home():
    return home()

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/genres')
def genres():
    return render_template('genres.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run()