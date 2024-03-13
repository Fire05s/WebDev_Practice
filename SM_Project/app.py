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
import random
from flask_moment import Moment

client = pymongo.MongoClient("mongodb+srv://[USER]:[PASSWORD]@cluster0.ookfz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.social_media

app = Flask(__name__)
moment = Moment (app)
app.secret_key = '279t8sklvsn'

session = {}

@app.route ('/',methods = ['GET','POST'])
def index ():
    if request.method == 'GET':
        return render_template ('/home.html')
    if request.method == 'POST':
        if 'regsub' in request.form:
            account = db.accounts.find_one ({'user':request.form ['reguser']})
            print (account)
            if account is None:
                print (2)
                dict1 = {}
                user = request.form ['reguser']
                pw = request.form ['regpw']
                pw = sha256_crypt.hash (pw)
                dict1 ['user'] = user
                dict1 ['pw'] = pw
                db.accounts.insert_one (dict1)
                flash ('Account created successfully.')
                return redirect ('/')
            else:
                flash ('Username is already being used.')
                return redirect ('/')
        if 'logsub' in request.form:
            # return request.form
            account = db.accounts.find_one ({'user':request.form ['loguser']})
            print (account)
            if account is None:
                flash ('Account not found.')
                return redirect ('/')
            else:
                if sha256_crypt.verify (request.form ['logpw'],account ['pw']):
                    session ['user'] = request.form ['loguser']
                    return redirect ('/landing')
                else:
                    flash ('Incorrect Password.')
                    return redirect ('/')

@app.route ('/landing',methods = ['GET','POST'])
def landing ():
    global session
    if 'user' not in session:
        flash ('You must login.')
        return redirect ('/')
    else:
        if request.method == 'GET':
            allposts = db.posts.find ()
            accounts = db.accounts.find ()
            followers = {}
            for account1 in accounts:
                followers [account1 ['user']] = 0
                for account2 in accounts:
                    if account1 != account2:
                        try:
                            if account1 ['user'] in account2 ['friends']:
                                followers [account1 ['user']] += 1
                        except:
                            pass
            return render_template ('/landing.html',allposts = allposts,session = session,followers = followers)
        if request.method == 'POST':
            if 'postsub' in request.form:
                try:
                    account = db.accounts.find_one ({'user':session ['user']})
                    print (account)
                    dict1 = {}
                    post = request.form ['postbody']
                    time = datetime.now ()
                    dict1 ['user'] = session ['user']
                    dict1 ['post'] = post
                    dict1 ['time'] = time
                    dict1 ['likes'] = 0
                    if request.form ['imglink'] != '':
                        imglink = request.form ['imglink']
                        dict1 ['imglink'] = imglink
                    db.posts.insert_one (dict1)
                    flash ('Post successfully made.')
                    return redirect ('/landing')
                except:
                    flash ('Please login before making a post.')
                    return redirect ('/landing')
            if 'profsub' in request.form:
                account = db.accounts.find_one ({'user':request.form ['postuser']})
                print (account)
                if account is None:
                    flash ('Account not found.')
                    return redirect ('/landing')
                else:
                    session ['viewing'] = account ['user']
                    return redirect ('/profile')
            if 'likesub' in request.form:
                post = db.posts.find_one ({'_id':ObjectId (request.form ['postid'])})
                print (post)
                if post is None:
                    flash ('Post not found.')
                    return redirect ('/landing')
                else:
                    if session ['user'] != post ['user']:
                        db.posts.update_one ({'_id':ObjectId (request.form ['postid'])},{'$set':{'likes':post['likes'] + 1}})
                        return redirect ('/landing')
                    else:
                        flash ('You cannot like your own post.')
                        return redirect ('/landing')
            if 'followsub' in request.form:
                account = db.accounts.find_one ({'user':session ['user']})
                post = db.posts.find_one ({'_id':ObjectId (request.form ['postid'])})
                if post is None:
                    flash ('Post not found.')
                    return redirect ('/landing')
                else:
                    if 'friends' not in account:
                        db.accounts.update_one ({'user':session ['user']},{'$set':{'friends':[post ['user']]}})
                    else:
                        if post ['user'] not in account ['friends']:
                            db.accounts.update_one ({'user':session ['user']},{'$push':{'friends':post ['user']}})
                        else:
                            flash ('You cannot follow a user more than once.')
                return redirect ('/landing')
            if 'logoutsub' in request.form:
                session = {}
                return redirect ('/')

@app.route ('/profile',methods = ['GET','POST'])
def profile ():
    global session
    if request.method == 'GET':
        userposts = list (db.posts.find ({'user':session ['viewing']}))
        followers = list (db.accounts.find ({'friends': {'$in': [session ['user']]}}))
        return render_template ('/profile.html',userposts = userposts,session = session,followers = followers)
    if request.method == 'POST':
        if 'followsub' in request.form:
            account = db.accounts.find_one ({'user':session ['user']})
            if 'friends' not in account:
                db.accounts.update_one ({'user':session ['user']},{'$set':{'friends':[session ['viewing']]}})
            else:
                if session ['user'] not in account ['friends']:
                    db.accounts.update_one ({'user':session ['user']},{'$push':{'friends':session ['viewing']}})
            return redirect ('/profile')
        if 'likesub' in request.form:
            post = db.posts.find_one ({'_id':ObjectId (request.form ['postid'])})
            print (post)
            if post is None:
                flash ('Post not found.')
                return redirect ('/profile')
            else:
                if session ['user'] != post ['user']:
                    db.posts.update_one ({'_id':ObjectId (request.form ['postid'])},{'$set':{'likes':post['likes'] + 1}})
                    return redirect ('/profile')
                else:
                    flash ('You cannot like your own post.')
                    return redirect ('/profile')
        if 'logoutsub' in request.form:
            session = {}
            return redirect ('/')
        if 'returnsub' in request.form:
            return redirect ('/landing')

@app.route ('/settings',methods = ['GET','POST'])
def settings ():
    global session
    if request.method == 'GET':
        return render_template ('/settings.html',session = session)
    if request.method == 'POST':
        if 'changesub' in request.form:
            if request.form ['changeuser'] != '':
                db.accounts.update_one ({'user':session ['user']},{'$set':{'user':request.form ['changeuser']}})
                db.posts.update_one ({'user':session ['user']},{'$set':{'user':request.form ['changeuser']}})
                # Changes the username of followers, not sure how to change usernames in the friends list
                # ,{'$set':{'user':request.form ['changeuser']}}
                friends = list (db.accounts.find ({'friends': {'$in': [session ['user']]}}))
                print ('friends',friends)
                for account in friends:
                    newfriends = account ['friends']
                    print ('newfriends original list',newfriends)
                    newfriends.remove (session ['user'])
                    newfriends.append (request.form ['changeuser'])
                    print (newfriends,'newfriends')
                    db.accounts.update_one ({'user':account ['user']},{'$set':{'friends':newfriends}})
                session ['user'] = request.form ['changeuser']
            if request.form ['profimg'] != '':
                db.accounts.update_one ({'user':session ['user']},{'$set':{'profimg':request.form ['profimg']}})
                db.posts.update_many ({'user':session ['user']},{'$set':{'profimg':request.form ['profimg']}})
            return redirect ('/settings')
        if 'logoutsub' in request.form:
            session = {}
            return redirect ('/')
        if 'returnsub' in request.form:
            return redirect ('/landing')

app.run (debug = True)