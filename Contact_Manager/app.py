from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from datetime import datetime
import pymongo
from bson.objectid import ObjectId
from flask import flash

client = pymongo.MongoClient("mongodb+srv://[USER]:[PASSWORD]@cluster0.ookfz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.contact_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdkljg8190t1'
#app = Flask ('note_manager',template_folder = 'templates')

@app.route ('/',methods = ['GET','POST'])
def index():
    if request.method == 'GET':
        contacts = db.contacts.find ()
        return render_template ('contacts.html',contacts = contacts)
    if request.method == 'POST':
        print (request.form)
        document = {}
        unique = True
        for loop in db.contacts.find():
            if request.form ['Name'] == loop ['Name']:
                flash ('Name already exists in contacts.')
                unique = False
        if unique == True:
            if len (request.form ['Name']) >= 3:
                try:
                    phone = int (request.form ['Phone Number'])
                    print ('phone type is',type (phone))
                    if type (request.form ['Email']) == type ('a') and '@' in request.form ['Email']:
                        document['Name'] = request.form ['Name']
                        document['Phone Number'] = phone
                        document['Email'] = request.form ['Email']
                        flash ('Contact successfully added.')
                        db.contacts.insert_one(document)
                    else:
                        flash ('Email needs to be a string and include "@".')
                except:
                    flash ('Phone Number must be numerical.')
            else:
                flash ('Name cannot have any numbers or the given name is too short (< 3).')
        return redirect('/')

@app.route ('/delete/<contact_id>')
def delete(contact_id):
    db.contacts.delete_one({'_id':ObjectId(contact_id)})
    flash ('Contact successfully deleted.')
    return redirect('/')

app.run (debug = True)