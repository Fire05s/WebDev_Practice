from flask import *
import json
import requests
app = Flask ('mars_discovery')

@app.route ('/')
def index():
    books = []
    if 'book' in request.args:
        search_word = request.args.get ('book')
        response = requests.get ("http://gutendex.com/books/?search=" + search_word)
        data = json.loads (response.content)
        books = data['results']
    return render_template ('home.html',books=books)
@app.route ('/home')
def home ():
    search_word = 'hyde'
    response = requests.get ("http://gutendex.com/books/?search=" + search_word)
    data = json.loads (response.content)
    print (data)
    return render_template ('home.html')

app.run (debug = True)