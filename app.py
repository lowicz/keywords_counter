from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import urllib2, re, trans

app = Flask(__name__)

class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def encoding_check(html_object):
    try:
        return html_object.headers['Content-Type'].split('charset=')[1]
    except:
        return 'utf8'

def encoding_page(html_text, enc):
    return html_text.decode(enc).encode('trans')

def parsing_page(html_text, enc):
    soup = BeautifulSoup(encoding_page(html_text, enc))
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
    return '\n'.join(chunk for chunk in chunks if chunk)


def get_keywords_list(html_text, enc):
    content = encoding_page(html_text, enc)
    keywordregex = re.compile("<meta name=\"[kK]eywords\".*?content=\"([^\"]*)\"")
    keywordlist = keywordregex.findall(content)
    if len(keywordlist) == 0:
        raise MyError("Page don't have keywords!")
    else:
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
        r = re.compile("\s".join(i.strip().lower().split(' ')))
        results[i] = len(re.findall(r, text.lower()))
    return results

@app.route('/', methods=['GET', 'POST'])
def home():
    error = results = None
    if request.method == 'GET': return render_template("index.html")
    if request.method == 'POST':
        try:
            if request.form['url'][:7] == 'http://':
                html_object = urllib2.urlopen(request.form['url'])
            else:
                html_object = urllib2.urlopen('http://'+request.form['url'])
            enc = encoding_check(html_object)
            html_text = html_object.read()
            try:
                keywords = get_keywords_list(html_text, enc)
                results = count_key(keywords, parsing_page(html_text, enc))
            except MyError as e:
                error = e.value
        except urllib2.URLError:
            error = "Wrong URL! Type correct adress"
    return render_template("index.html", results=results, error=error)

if __name__ == '__main__':
    app.run(debug=True)
