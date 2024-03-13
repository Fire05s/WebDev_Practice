from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from datetime import datetime
import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb+srv://[USER]:[PASSWORD]]@cluster0.ookfz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.note_manager

app = Flask(__name__)
#app = Flask ('note_manager',template_folder = 'templates')

@app.route ('/',methods = ['GET','POST'])
def index():
    if request.method == 'GET':
        notes = db.notes.find ()
        return render_template ('My_Notes.html',notes = notes)
    if request.method == 'POST':
        print (request.form)
        document = {}
        document['note'] = request.form ['note']
        document['timestamp'] = datetime.now()
        db.notes.insert_one(document)
        return redirect('/')

@app.route ('/delete/<note_id>')
def delete(note_id):
    db.notes.delete_one({'_id':ObjectId(note_id)})
    return redirect('/')

app.run (debug = True)