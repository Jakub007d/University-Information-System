from flask import render_template, request, redirect,url_for
from app import app
from app.forms import LoginForm
import psycopg2

@app.route('/login',methodes=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('index.html')