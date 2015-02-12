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

	checkbTitle = []

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
		fLikes = soup.findAll('a', {'class':'j-meta-number', 'data-command':'showLikes', 'data-object-type':'38'})
		mLikes = unicode.join(u'\n', map(unicode,fLikes))

		soup = BeautifulSoup(''.join(mLikes))

		soupTitle = BeautifulSoup(page.text)
		# finding title scraping goes here
		bTitle = soupTitle.findAll('tr',{'data-object-type':'38'})
		# mTitle = unicode.join(u'\n', map(unicode,bTitle))

		# soupTitle = BeautifulSoup(''.join(mTitle))


		for i in range(len(soup.findAll('a'))):
			likesArr.append(int(''.join(soup.findAll('a')[i].contents)))

		for i in range(len(bTitle)):
			checkbTitle += soupTitle.findAll('tr',{'data-object-type':'38'})[i].findAll('a')[0].contents

		for i in range(len(bTitle)):
			likesArr.append(checkbTitle[i].encode('ascii','ignore'))
			
		# checkmTitle = unicode.join(u'\n', map(unicode,checkbTitle))
		# soupTitle = BeautifulSoup(''.join(checkmTitle))
		# likesArr.append(str(''.join(soupTitle.contents)))	

	return Response(json.dumps(likesArr),  mimetype='application/json')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html',name=name)

if __name__ == '__main__':
	app.run()


for i in range(16):
	checkbTitle += soup.findAll('tr',{'data-object-type':'38'})[i].findAll('a')[0].contents

uconvert = unicode.join(u'\n', map(unicode,checkbTitle))
uconvert.encode('ascii','ignore')
arrconvert = uconvert.split('\n')
likesArr.append(arrconvert)