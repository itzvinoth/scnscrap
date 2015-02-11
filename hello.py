import json

import requests
from flask import Flask
from flask import render_template, Response
from BeautifulSoup import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/arr/')
def array():

	likesArr = []
	pagination = 0
	base_url = "http://scn.sap.com/people/mike.howles4/content"

	while True:
		# Request page with params `start`
		# ex. http://scn.sap.com/people/mike.howles4/content?start=20
		page = requests.get(base_url, params={"start":str(pagination)})
		soup = BeautifulSoup(page.text)

		# Get author name
		author = soup.title.string.split("'s")[0].strip()

		if page.text.find(author+" has not created any content yet") == -1:
			pagination += 20
		else:
			break

		# finding no. of likes and converting format
		fLikes = soup.findAll('a', {'class':'j-meta-number', 'data-command':'showLikes'})
		mLikes = unicode.join(u'\n', map(unicode,fLikes))

		soup = BeautifulSoup(''.join(mLikes))

		for i in range(len(soup.findAll('a'))):
			likesArr.append(int(''.join(soup.findAll('a')[i].contents)))

	return Response(json.dumps(likesArr),  mimetype='application/json')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html',name=name)

if __name__ == '__main__':
	app.run()
