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

client = pymongo.MongoClient("mongodb+srv://[USER]:[PASSWORD]@cluster0.ookfz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.shop

app = Flask(__name__)
app.secret_key = '279t8sklvsn'

session = {}

@app.route ('/shop',methods = ['GET','POST'])
def shop ():
    if 'email' not in session:
        flash ('You must login.')
        return redirect ('/')
    else:
        if request.method == 'GET':
            items = list (db.stock.find ({'email': session ['email']}))
            # print (items)
            return render_template ('shop.html',session = session,items = items)
        if request.method == 'POST':
            if 'logout' in request.form:
                del session ['email']
                return redirect ('/')
            elif 'add' in request.form:
                print (1)
                dict1 = {}
                item = request.form ['item']
                desc = request.form ['description']
                email = request.form ['emailadd']
                price = request.form ['price']
                quantity = request.form ['quantity']
                img = request.form ['image']
                dict1 ['item'] = item
                dict1 ['desc'] = desc
                dict1 ['email'] = email
                dict1 ['price'] = price
                dict1 ['quantity'] = quantity
                dict1 ['img'] = img
                db.stock.insert_one (dict1)
                flash ('Item added successfully.')
                return redirect ('/shop')
            elif 'addstock' in request.form:
                print (request.form ['itemid'])
                additem = db.stock.find_one ({'_id':ObjectId (request.form ['itemid'])})
                additem ['quantity'] = int (additem ['quantity']) + int (request.form ['addq'])
                print (additem ['quantity'])
                db.stock.update_one ({'_id':ObjectId (request.form ['itemid'])},{'$set':{'quantity':additem ['quantity']}})
                return redirect ('/shop')

@app.route ('/visit',methods = ['GET','POST'])
def visit ():
    if request.method == 'GET':
        shopid = request.args.get ('shopid')
        account = db.accounts.find_one ({'_id':ObjectId (shopid)})
        items = list (db.stock.find ({'email':account ['email']}))
        return render_template ('visit.html',account = account,items = items)
    if request.method == 'POST':
        if 'home' in request.form:
            return redirect ('/')
        elif 'addcart' in request.form:
            pass

@app.route ('/cart',methods = ['GET','POST'])
def cart ():
    if request.method == 'GET':
        cart = db.cart.find_one ({'cartid':session ['cartid']})
        print (cart)
        final = 0
        contents = cart['cart']
        for loop in contents:
            final += float (loop ['quantity']) * float (loop ['price'])
        return render_template ('checkout.html',contents = contents,final = final)
    if request.method == 'POST':
        if 'home' in request.form:
            return redirect ('/')
        elif 'checkout' in request.form:
            del session ['cartid']
            return redirect ('/')

@app.route ('/',methods = ['GET','POST'])
def index ():
    cartid = random.randint (1000,9999)
    if request.method == 'GET':
        if 'cartid' not in session:
            db.cart.insert_one ({'cart':[],'cartid':cartid})
            session ['cartid'] = cartid
        cart_count = len (db.cart.find_one ({'cartid': session ['cartid']}))
        print ('cart_count',cart_count,db.cart.find_one ({'cartid': session ['cartid']}))
        stores = db.accounts.find ()
        items = db.stock.find ()
        return render_template ('home.html',stores = stores,items = items)
    if request.method == 'POST':
        if 'signup' in request.form:
            print (1)
            account = db.accounts.find_one ({'email':request.form ['email']})
            print (account)
            if account is None:
                print (2)
                dict1 = {}
                shop = request.form ['shop']
                owner = request.form ['owner']
                email = request.form ['email']
                passw = request.form ['password']
                passw = sha256_crypt.hash (passw)
                dict1 ['shop'] = shop
                dict1 ['owner'] = owner
                dict1 ['email'] = email
                dict1 ['passw'] = passw
                db.accounts.insert_one (dict1)
                flash ('Account created successfully.')
            else:
                flash ('Email is already being used.')
        elif 'login' in request.form:
            account = db.accounts.find_one ({'email':request.form ['email']})
            print (account)
            if account is None:
                flash ('Account not found.')
                return redirect ('/')
            else:
                if sha256_crypt.verify (request.form ['password'],account ['passw']):
                    session ['email'] = request.form ['email']
                    session ['shop'] = account ['shop']
                    return redirect ('/shop')
                else:
                    flash ('Incorrect Password.')
                    return redirect ('/')
        elif 'visit' in request.form:
            print (request.form ['vstore'])
            account = db.accounts.find_one ({'_id':ObjectId (request.form ['vstore'])})
            return redirect ('/visit?shopid=' + str (account ['_id']))
        elif 'addcart' in request.form:
            print (request.form ['itemid'])
            additem = db.stock.find_one ({'_id':ObjectId (request.form ['itemid'])})
            print (additem)
            item = {'name':additem ['item'],'quantity':request.form ['qcart'],'price':additem ['price'],'total':float (request.form ['qcart']) * float (additem ['price'])}
            print (session)
            db.cart.update_one ({'cartid':session ['cartid']},{'$addToSet':{'cart': item}})
            additem ['quantity'] = int (additem ['quantity']) - int (request.form ['qcart'])
            print (additem ['quantity'])
            db.stock.update_one ({'_id':ObjectId (request.form ['itemid'])},{'$set':{'quantity':additem ['quantity']}})
            return redirect ('/')
        elif 'viewcart' in request.form:
            return redirect ('/cart')
        return redirect ('/')
if __name__ == '__main__':
    app.run ()