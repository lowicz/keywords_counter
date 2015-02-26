from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import urllib2
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
	results = ''
	if request.method == 'POST':
		url = request.form['url']
		htmlobj = urllib2.urlopen(url)
		encoding=htmlobj.headers['Content-Type'].split('charset=')[1]
		ucontent = unicode(htmlobj.read(), encoding)
		keywordregex = re.compile("<meta name=\"Keywords\".*?content=\"([^\"]*)\"")
		keywordlist = keywordregex.findall(ucontent)
    	results =  keywordlist
	return render_template("index.html", results=results)

if __name__ == '__main__':
	app.run(debug=True)