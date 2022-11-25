from flask import render_template, request, redirect,url_for
from app import app

@app.route('/login', methods = ['GET','POST'])

def login():


    #if request.method == 'POST':
    #    if request.form['username'] != 'miguel' or request.form['password'] != 'sanchez':
    error = 'Invalid Credentials. Please try again.'
    #    else:
    #        return redirect(url_for('login'))

    return render_template('index.html', error=error)


@app.route('/', methods=['GET','POST'])
def mainPage():
    return render_template('homePage.html')
