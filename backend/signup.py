import smtplib

import backend.utils.db as utils
import backend.utils.get_links as links

from flask import render_template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def signup(request, session):
	if 'username' not in request.form:
		return render_template('signup.html', flag = False)
	else:
		db =  utils.pysqlite3()	
		print ("dati inseriti")	
		username = request.form['username'].title()
		first_name = request.form['first_name'].title()
		second_name = request.form['second_name'].title()
		password = request.form['password']
		confirm_password = request.form['confirm_password']
		email = request.form['email']
		confirm_email = request.form['confirm_email']
		
		if password == confirm_password:
			if email == confirm_email:

				query = """
				SELECT username
				FROM utente
				WHERE username = '{}'
				COLLATE NOCASE
				""".format(username)
				result = db.query_db(query)

				try:
					tmp = result[0][0]
					flag = False
				except:
					flag = True

				if flag:
					query = """
					SELECT email
					FROM utente
					WHERE email = '{}'
					COLLATE NOCASE
					""".format(email)
					result = db.query_db(query)

					try:
						tmp = result[0][0]
						flag = False
					except:
						flag = True

					if flag:
						query = """
						INSERT INTO utente
						VALUES (NULL, '%s', '%s', '%s', '%s', '%s', 'None', 0)
						""" % (username, first_name, second_name, password, email)
						db.query_db(query)

						query = """
						SELECT seq
						FROM sqlite_sequence
						WHERE name = "utente"
						"""
						user_id = db.query_db(query)[0][0]

						secret_key = links.id_generator(10)
						query = "INSERT INTO conferma VALUES ('{}', {})".format(secret_key, user_id)
						db.query_db(query)

						send_mail(email, username, secret_key)
					else:
						return render_template('signup.html', flag = False, error = True, content = "Email già esistente")
				else:
				    return render_template('signup.html', flag = False, error = True, content = "Username già esistente")			 
				return render_template('signup.html', flag = True)
			else:
				return render_template('signup.html', flag = False, error = True, content = "Le email inserite non sono uguali")
		else:
			return render_template('signup.html', flag = False, error = True, content = "Le password inserite non sono uguali")


def send_mail(user_email, username, secret_key):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("tesinagarau@gmail.com", "Paolopoalo97")

	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Registrazione a tesinagarau"
	msg['From'] = "tesinagarau@gmail.com"
	msg['To'] = user_email

	text = "Link per la registrazione su tesinagarau.pythonanywhere.com"
	html = """\
	<html>
	  <head></head>
	  <body>
	    <h3>Ciao <b>{}</b>!<br><br>
	        Grazie per esserti registrato su tesinagarau.pythonanywhere.com!<br><br>
	        Ecco il link per confermare la tua registrazione: 
	        <a href="tesinagarau.pythonanywhere.com/signup/{}">
	        	tesinagarau.pythonanywhere.com/signup/{}
	        </a>.
	        OR
	        <a href="127.0.0.1:5000/signup/{}">
	        	127.0.0.1:5000/signup/{}
	        </a>.
	    </h3>
	  </body>
	</html>
	""".format(username, secret_key, secret_key, secret_key, secret_key)

	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	msg.attach(part1)
	msg.attach(part2)

	#msg = "YOUR MESSAGE!"
	server.sendmail("tesinagarau@gmail.com", user_email, msg.as_string())
	server.quit()