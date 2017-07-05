import smtplib
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
'''
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("tesinagarau@gmail.com", "Paolopoalo97")
 
msg = "YOUR MESSAGE!"
server.sendmail("tesinagarau@gmail.com", "crig97@gmail.com", msg)
server.quit()
'''
'''
import string
import random
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
print(id_generator())
print(id_generator(3, "611"))
'''
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
	    </h3>
	  </body>
	</html>
	""".format(username, secret_key, secret_key)

	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	msg.attach(part1)
	msg.attach(part2)

	#msg = "YOUR MESSAGE!"
	server.sendmail("tesinagarau@gmail.com", user_email, msg.as_string())
	server.quit()

send_mail("crig97@gmail.com", "UsernameDiProva", "KEYKEYKEY7")