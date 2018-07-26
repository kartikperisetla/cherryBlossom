import csv
import shutil, os
from flask import Flask, render_template, request, redirect, url_for
import requests, simplejson, json, base64
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
    #return redirect('/0')
    return render_template("index.html")


@app.route('/0', methods=['POST', 'GET'])
def image_upload(ind=None):
    print('Image upload request received')
    if request.method == 'POST':

        if 'file' not in request.files:
            print('No file found')
            return render_template("index.html")

        file = request.files['file']

        if file.filename == '':
            print('No selected file')
            return render_template("index.html")
        if file and allowed_file(file.filename):
            filename = file.filename
            print(filename, type(file))
            # with open('picture_out.png', 'wb') as f:
                # f.write(file)
            # send file to second endpoint
    return render_template("index.html")

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/goto', methods=['POST', 'GET'])
def goto():
    if request.method == 'POST':
        data = request.form['queryStr']
    if request.method == 'GET':
        data = request.args.get('queryStr')
    reqUrl = "https://pensieve3.search.windows.net/indexes/gringottsv2/docs?api-version=2017-11-11&search=" + data
    headers = {
        'api-key': 'B91A6F1F83847E85E94C2F87488DC059'
    }
    req = requests.get(reqUrl, headers=headers)
    jsonObj = simplejson.loads(req.content)
    imagesListFromJson = jsonObj['value']

    print("Query String:", data)
    print("Number of images returned:", len(imagesListFromJson))
    # if (len(imagesListFromJson) > 0):
        # for fileName in os.listdir('images'):
            # os.remove(os.getcwd() + "\\images\\" +fileName)
    imageDict = {}
    for i in range(len(imagesListFromJson)):
        imageDict[str(i)] = { 'image' : imagesListFromJson[i]['image'], 'caption': imagesListFromJson[i]['caption']}
        # imgdata = base64.b64decode(imagesListFromJson[i]['image'])
        # filename = "images/" + imagesListFromJson[i]['filename']
        # with open(filename, 'wb') as f:
            # f.write(imgdata)

    return json.dumps(imageDict)

if __name__ == '__main__':
    app.run(debug=True)
