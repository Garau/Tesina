import itunespy
import backend.utils.db as utils

from flask import render_template

def signup(request, session):
	if 'username' not in request.form:
		return render_template('signup.html', flag = False)
	else:	
		print ("dati inseriti")	
		username = request.form['username']
		first_name = request.form['first_name']
		second_name = request.form['second_name']
		password = request.form['password']
		confirm_password = request.form['confirm_password']
		email = request.form['email']
		confirm_email = request.form['confirm_email']
		
		if password == confirm_password:
			if email == confirm_email:
				query = """
					INSERT INTO utente
					VALUES (NULL, '%s', '%s', '%s', '%s', '%s')
					""" % (username, first_name, second_name, password, email)
				print (query)
				db =  utils.pysqlite3()
				db.query_db(query)
				return render_template('signup.html', flag = True)
			else:
				return render_template('signup.html', flag = False, error = True, content = "Le email inserite non sono uguali")
		else:
			return render_template('signup.html', flag = False, error = True, content = "Le password inserite non sono uguali")