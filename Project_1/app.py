import flask
from flask import request
from flask import render_template
from flask import Flask

app = Flask(__name__)
@app.route('/',methods = ['GET','POST'])
def base ():
    if request.method == 'GET':
        username = 'Bob'
        return render_template ('hello.html',username = username)
@app.route('/cart',methods = ['GET','POST'])
def cart ():
    if request.method == 'GET':
        cart = [
            {
                'name':'Apple',
                'price':5,
                'quantity':3
            },
            {
                'name':'Pear',
                'price':4,
                'quantity':6
            },
            {
                'name':'banana',
                'price':7,
                'quantity':2
            }
        ]
        return render_template('cart.html', items = cart)
@app.route ('/gallery')
def gallery ():
    items = [
        {
            'type':'image',
            'title':'Computer',
            'url':r'https://www.google.com/imgres?imgurl=https%3A%2F%2Fcdn.britannica.com%2F77%2F170477-050-1C747EE3%2FLaptop-computer.jpg&imgrefurl=https%3A%2F%2Fwww.britannica.com%2Ftechnology%2Fcomputer&tbnid=_bAxRLesPf9HpM&vet=12ahUKEwigk4ya2c73AhW-FTQIHckWDQIQMygAegUIARCYAg..i&docid=9oCv57c03X8yLM&w=1600&h=1097&q=computer&ved=2ahUKEwigk4ya2c73AhW-FTQIHckWDQIQMygAegUIARCYAg'
        },
        {
            'type':'audio',
            'title':'Test Audio',
            'url':r'C:\Users\Brandon Tsai\OneDrive\Desktop\Web Development\Project_1\static\Correct_Sound.mp3'
        },
        {
            'type':'video',
            'title':'Earth',
            'url':r'C:\Users\Brandon Tsai\OneDrive\Desktop\Web Development\Project_1\static\shark_video.mp4'
        }
    ]
    return render_template('gallery.html', items = items)
if __name__ == '__main__':
    app.run (debug = True)