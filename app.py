from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import urllib2, re, trans

app = Flask(__name__)

def encoding_check(html_object):
		try:
			return html_object.headers['Content-Type'].split('charset=')[1]
		except:
			return 'utf8'	

def encoding_page(html_text, enc):
	return html_text.decode(enc).encode('trans')

def get_keywords_list(html_text, enc):
	content = encoding_page(html_text, enc)
	keywordregex = re.compile("<meta name=\"Keywords\".*?content=\"([^\"]*)\"")
	keywordlist = keywordregex.findall(content)
	return str(keywordlist)[3:-2].split(',')

@app.route('/', methods=['GET', 'POST'])
def home():
	results = ''
	html_object = ''
	if request.method == 'POST':
		html_object = urllib2.urlopen(request.form['url'])
		enc = encoding_check(html_object)
		html_text = html_object.read()
    	keywords = get_keywords_list(html_text, enc)
    	soup = BeautifulSoup(encoding_page(html_text, enc))
    	results = soup.get_text()
	return render_template("index.html", results=results)

if __name__ == '__main__':
	app.run(debug=True)