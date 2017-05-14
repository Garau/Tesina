from flask import redirect
from flask import url_for

def logout(request, session):
	session.clear()
	return redirect(url_for('route_home'))