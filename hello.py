import json
import urllib2
from BeautifulSoup import BeautifulSoup
from flask import Flask
from flask import render_template, Response
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World!'
	
@app.route('/arr/')
def array():
	#data = {"key1": "value1", "key2": "value2", "key3": "value3"}
	#data = [2,1,3,5]
	#return Response(json.dumps(data),  mimetype='application/json')

	likesArr = []
	i = 0
	# #Scraping code goes here.... 
	page = urllib2.urlopen("http://scn.sap.com/people/mike.howles4/content")
	soup = BeautifulSoup(''.join(page))

	if soup.findAll('a',{'class':'j-pagination-next'}):
		while i<2:
			
			link = "http://scn.sap.com/people/mike.howles4/content?start=" + str((i+1)*20)
			if link.find("http") != -1 & i == 1:
				linkTest = "http://scn.sap.com/people/mike.howles4/content?start=20"
				link.replace(linkTest,'')
			#link.replace("http://scn.sap.com/people/mike.howles4/content?start=" + str((i)*20),'')
			page = urllib2.urlopen(link)
			soup = BeautifulSoup(''.join(page))
			fLikes = soup.findAll('a', {'class':'j-meta-number', 'data-command':'showLikes'})
			mLikes = unicode.join(u'\n',map(unicode,fLikes))

			soup = BeautifulSoup(''.join(mLikes))

			for i in range(len(soup.findAll('a'))):
				likesArr.append(int(''.join(soup.findAll('a')[i].contents)))

			
			return Response(json.dumps(likesArr),  mimetype='application/json')

			i += 1	

	#soup = BeautifulSoup(''.join(page))

	# #finding no. of likes and converting format
	fLikes = soup.findAll('a', {'class':'j-meta-number', 'data-command':'showLikes'})
	mLikes = unicode.join(u'\n',map(unicode,fLikes))

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

	#	span title="likes"	<a class="j-meta-number"

	#soup.find("b", { "class" : "lime" })
	#test = soup.findAll('a',{'class':'j-meta-number','data-command':'showLikes'})
	#test1 = unicode.join(u'\n',map(unicode,test))
	#soup = BeautifulSoup(''.join(test1))
	#print soup.prettify()