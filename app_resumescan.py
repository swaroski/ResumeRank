

#################################################################################################################################################




"""

Prerequisites

    Gensim
    Numpy==1.11.3
    Pandas
    Sklearn
    Dash
    Antiwords
    autocorrect




        To Run this code: 
            # python app.py

	And open URL localhost:5000


"""

import glob
import os
import warnings
import textract
import requests
from flask import (Flask,session, g, json, Blueprint,flash, jsonify, redirect, render_template, request,
                   url_for, send_from_directory)
from gensim.summarization import summarize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from werkzeug import secure_filename
from flask_login import LoginManager, login_user, current_user, logout_user

import pdf2txt as pdf
import PyPDF2

#import screen
import search
import hashlib
from wtform_fields import *
from models import *
from passlib.hash import pbkdf2_sha256

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

app = Flask(__name__)

DATABASE_URL= "postgresql://postgres:postgres@127.0.0.1/intervai"

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#app.config['UPLOAD_FOLDER'] = 'Original_Resumes/'
app.config['UPLOAD_FOLDER'] = 'Upload-Resume'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Initialize login manager
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class jd:
    def __init__(self, name):
        self.name = name

def getfilepath(loc):
    temp = str(loc).split('\\')
    return temp[-1]
    
@app.route("/register", methods=['GET', 'POST'])
def register():
    
    
    reg_form = RegistrationForm()
    #print(reg_form.errors)
    
    # Update database if validation success
    if reg_form.validate_on_submit():
        
        username = reg_form.username.data
        password = reg_form.password.data

        # Hash password
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add username & hashed password to DB
        user = User(username=username, hashed_pswd=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))
    print(reg_form.errors)
    return render_template("register.html", form=reg_form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        session['logged_in'] = True
        return redirect(url_for('home'))
    print(login_form.errors)
    return render_template("login.html", form=login_form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))


@app.route('/')
def home():
    x = []
    for file in glob.glob("./Job_Description/*.txt"):
        res = jd(file)
        x.append(jd(getfilepath(file)))
    print(x)
    return render_template('index.html', results = x)

@app.route('/uploadResume', methods=['GET', 'POST'])
def uploadResume():
    return render_template('uploadresume.html')


@app.route('/results', methods=['GET', 'POST'])
def res():
    if request.method == 'POST':
        jobfile = request.form['des']
        print(jobfile)
        flask_return = screen.res(jobfile)
        
        print(flask_return)
        return render_template('result.html', results = flask_return)



@app.route('/resultscreen' ,  methods = ['POST', 'GET'])
def resultscreen():
    if request.method == 'POST':
        jobfile = request.form.get('Name')
        print(jobfile)
        flask_return = search.res(jobfile)
        return render_template('result.html', results = flask_return)



@app.route('/resultsearch' ,methods = ['POST', 'GET'])
def resultsearch():
    if request.method == 'POST':
        search_st = request.form.get('Name')
        print(search_st)
    result = search.res(search_st)
    # return result
    return render_template('result.html', results = result)


@app.route('/Original_Resume/<path:filename>')
def custom_static(filename):
    return send_from_directory('./Original_Resumes', filename)



if __name__ == '__main__':
   # app.run(debug = True) 
    # app.run('127.0.0.1' , 5000 , debug=True)
    app.run('0.0.0.0' , 5000 , debug=True , threaded=True)
    
