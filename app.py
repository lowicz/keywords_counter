"""This application counts how many times
webpage keywords are apears in page content.

Author: Jakub Lowicki
jakub.lowicki@hotmail.com"""

from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import urllib2
import re
import trans

app = Flask(__name__)

###########
# HELPERS #
###########


def encoding_check(html_object):
    """Check page encoding."""

    try:
        return html_object.headers['Content-Type'].split('charset=')[1]
    except:
        return 'utf8'


def parsing_page(html_text, enc):
    """Getting visual content of page using bs4."""

    soup = BeautifulSoup(html_text.decode(enc).encode('trans'))
    for script in soup(["script", "style"]):
        script.extract()
    return soup.get_text()


def get_keywords_list(html_text, enc):
    """Getting list of webpage keywors."""

    soup = BeautifulSoup(html_text.decode(enc).encode('trans').lower())
    return soup.find("meta", {"name": "keywords"})['content'].split(',')


def count_key(keywords, text):
    """Keywords Counter."""
    results = {}
    for i in keywords:
        r = re.compile("\s".join(i.strip().lower().split(' ')))
        results[i] = len(re.findall(r, text.lower()))
    return results

###########
# ROUTING #
###########


@app.route('/', methods=['GET', 'POST'])
def home():
    """Render Templates, and execute helpers."""
    error = results = None

    if request.method == 'GET':
        return render_template("index.html")

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
            except TypeError:
                error = "Page don't have keywords!"
        except urllib2.URLError:
            error = "Wrong URL! Type correct adress"
    return render_template("index.html", results=results, error=error)

if __name__ == '__main__':
    app.run(debug=True)
