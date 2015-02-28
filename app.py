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

def remove_spaces(s):
	if s[0] == ' ':
		return s[1:]
	elif s[-1] == ' ':
		return s[:-1]
	else: return s

def count_key(keywords, text):
	results = {}
	for i in keywords:
		r = re.compile(remove_spaces(i))
		results[i] = len(re.findall(r, text))
	return results

@app.route('/', methods=['GET', 'POST'])
def home():
	enc = 'utf8'
	if request.method == 'GET': return render_template("index.html")
	if request.method == 'POST':
		html_object = urllib2.urlopen(request.form['url'])
		enc = encoding_check(html_object)
		html_text = html_object.read()
    	keywords = get_keywords_list(html_text, enc)
    	soup = BeautifulSoup(encoding_page(html_text, enc))
    	results = count_key(keywords, soup.get_text())
	return render_template("index.html", results=results)

if __name__ == '__main__':
	app.run(debug=True)