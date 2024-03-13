from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from datetime import datetime
import pymongo
from bson.objectid import ObjectId
from flask import flash
import random

client = pymongo.MongoClient("mongodb+srv://[USER]:[PASSWORD]@cluster0.ookfz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.jumbled

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdkljg8190t1'

@app.route ('/',methods = ['GET','POST'])
def index():
    if request.method == 'GET':
        words = db.words.find ()
        return render_template ('jumbled.html',words = words)
    if request.method == 'POST':
        print (request.form)
        document = {}
        document['word'] = request.form ['word']
        if request.form ['word'] != '':
            db.words.insert_one(document)
            flash ('Word added successfully.')
        else:
            flash ('Please add a word.')
        return redirect('/')

@app.route ('/play',methods = ['GET','POST'])
def play ():
    if request.method == 'GET':
        words = list (db.words.find ())
        print (words)
        sendlist = []
        while len (sendlist) < 5 or len (sendlist) >= len (words):
            present = False
            selection = random.choice (words)
            for loop in sendlist:
                if loop ['_id'] == selection ['_id']:
                    present = True
            if present == False:
                jumbledlist = list (selection ['word'])
                random.shuffle (jumbledlist)
                jumbledword = ''.join (jumbledlist)
                dict1 = {'_id': selection ['_id'],'word':jumbledword}
                sendlist.append (dict1)
                #print (sendlist)
        return render_template ('play.html',words = sendlist)
    if request.method == 'POST':
        points = 0
        useranswer = []
        correctanswers = []
        print ('request.form',request.form)
        for loop in request.form:
            if loop != 'submit':
                correctdict = db.words.find_one ({'_id':ObjectId(loop)})
                if correctdict ['word'] == request.form [loop]:
                    points += 1
                useranswer.append (request.form [loop])
                correctanswers.append (correctdict ['word'])
        print ('points',points)
        return render_template ('result.html',points = points, user_answer = useranswer,correct_answer = correctanswers)
app.run (debug = True)