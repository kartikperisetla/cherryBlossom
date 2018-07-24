import csv
from flask import Flask, render_template, request, redirect, url_for
import requests
import simplejson
from pager import Pager


def read_table(url):
    """Return a list of dict"""
    # r = requests.get(url)
    with open(url) as f:
        return [row for row in csv.DictReader(f.readlines())]


APPNAME = "Occipital Lobe"
STATIC_FOLDER = 'static'
TABLE_FILE = "static/fakecatalog.csv"

table = read_table(TABLE_FILE)
pager = Pager(len(table))


app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config.update(
    APPNAME=APPNAME,
    )


@app.route('/')
def index():
    return redirect('/0')


@app.route('/<int:ind>/')
def image_view(ind=None):
    if ind >= pager.count:
        return render_template("404.html"), 404
    else:
        pager.current = ind
        return render_template(
            'imageview.html',
            index=ind,
            pager=pager,
            data=table[ind],
            searchQueryString="N/A")


@app.route('/goto', methods=['POST', 'GET'])
def goto():
    data = request.form.get('searchQuery')
    print (data)
    reqUrl = "https://pensieve3.search.windows.net/indexes/goblins/docs?api-version=2017-11-11&search=" + data
    headers = {
        'api-key': 'B91A6F1F83847E85E94C2F87488DC059'
    }
    req = requests.get(reqUrl, headers=headers)
    jsonObj = simplejson.loads(req.content)
    print (jsonObj)
    ind = 3;
    pager.current = ind
    return render_template(
        'imageview.html',
        index=ind,
        pager=pager,
        data=table[ind],
        searchQueryString=data)


if __name__ == '__main__':
    app.run(debug=True)
