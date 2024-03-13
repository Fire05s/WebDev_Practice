from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from datetime import datetime
import pymongo
from bson.objectid import ObjectId
from passlib.hash import sha256_crypt
from flask import flash
from flask import sessions

client = pymongo.MongoClient("mongodb+srv://[USER]:[PASSWORD]@cluster0.ookfz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.logins

app = Flask(__name__)
app.secret_key = '891570328ssc'

session = {}

@app.route ('/home',methods = ['GET','POST'])
def home():
    if 'email' not in session:
        flash ('You must login')
        return redirect ('/')
    else:
        if request.method == 'GET':
            return render_template ('home.html',session = session)
        if request.method == 'POST':
            del session ['email']
            return redirect ('/')

@app.route ('/',methods = ['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template ('login.html')
    if request.method == 'POST':
        #return (request.form)
        if 'signup' in request.form:
            print (1)
            account = db.logins.find_one ({'email':request.form ['email']})
            print (account)
            if account is None:
                print (2)
                dict1 = {}
                fname = request.form ['fname']
                lname = request.form ['lname']
                email = request.form ['email']
                passw = request.form ['password']
                passw = sha256_crypt.hash (passw)
                dict1 ['fname'] = fname
                dict1 ['lname'] = lname
                dict1 ['email'] = email
                dict1 ['passw'] = passw
                db.logins.insert_one (dict1)
                flash ('Account created successfully.')
            else:
                flash ('Email is already being used.')
        elif 'login' in request.form:
            account = db.logins.find_one ({'email':request.form ['email']})
            print (account)
            if account is None:
                flash ('Account not found.')
                return redirect ('/')
            else:
                if sha256_crypt.verify (request.form ['password'],account ['passw']):
                    # flash ('Correct')
                    session ['email'] = request.form ['email']
                    return redirect ('/home')
                else:
                    flash ('Incorrect Password.')
                    return redirect ('/')
        #db.words.insert_one(document)
        return redirect('/')

app.run (debug = True)