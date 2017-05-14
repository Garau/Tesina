import itunespy

from flask import render_template

def home():

	artist = itunespy.search_artist('NOFX')
	albums = artist[0].get_albums()

	#image = ('../static/electric_sea.jpg','../static/ok_computer.jpg','../static/in_the_aeroplane_over_the_sea.jpg','../static/scenes_from_a_memory.jpg')
	image1 = albums[0].artwork_url_100.replace('100','600')
	image2 = albums[1].artwork_url_100.replace('100','600')
	image3 = albums[2].artwork_url_100.replace('100','600')
	image4 = albums[3].artwork_url_100.replace('100','600')

	image = (image1, image2, image3, image4)

	print (image)
	return render_template('home.html', image=image)