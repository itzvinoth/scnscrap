import json
import re

import requests
from flask import Flask
from flask import render_template, Response
from BeautifulSoup import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/arr/')
def array():

	data = []
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

		# return soup

		rows = soup.find(
			'table', attrs={'class':'j-browse-list'}).find('tbody').findAll('tr')

		for row in rows:
			icon_class = row.find('td', attrs={'class':'j-td-icon'}).find(
				'img', attrs={'class':re.compile(r".*\bjive-icon-blog\b.*")})

			if icon_class is not None:
				row_title = row.find('td', attrs={'class':'j-td-title'}).find('a')
				row_title_text = row_title.text.encode('ascii','ignore')
				row_title_link = row_title['href'].encode('ascii','ignore')
				row_likes = int(row.find(attrs={'data-command':'showLikes'})['data-count'])
				row_bookmarks = int(row.find(attrs={'data-command':'showBookmarks'})['data-count'])
				row_views = int(row.find('td', attrs={
					'class':re.compile(r".*\bj-td-views\b.*")
					}).find('span').contents[0])

				data.append({
					'title': row_title_text,
					'link': row_title_link,
					'likes': row_likes,
					'bookmarks': row_bookmarks,
					'views': row_views
					})

	return Response(json.dumps(data),  mimetype='application/json')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html',name=name)

if __name__ == '__main__':
	app.run()
