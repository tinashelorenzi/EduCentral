from flask import Flask, render_template, request, redirect, session, jsonify
import os, sqlite3
from handlers import login_handler,cipherguard, database_handler

from cs50 import SQL
app = Flask(__name__)
enckey = "95fb144ffdb4a1899ce187a015ec02a21a227018"
app.secret_key = 'Shall I compare thee to a summers day'

@app.route("/")
def index():
    if session.get('authenticated'):
        return redirect('dashboard')
    else:
        return render_template('login.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        encrypted = cipherguard.encrypt_pass(password,enckey)
        if login_handler.authenticate(username,encrypted) != 0:
            id = login_handler.authenticate(username,encrypted)
            session['userid'] = id
            session['authenticated'] = True
            return redirect("/dashboard")
        else:
            return "Incorrect credentials"
        
@app.route('/dashboard')
def dashboard():
    if session.get('authenticated'):
        id = session.get('userid')
        username = database_handler.if_fetch_name(id)
        total_learners = database_handler.learner_count()
        total_parents = database_handler.parent_count()
        return render_template("dashboard.html",username=username,learner_count=total_learners,parent_count=total_parents)
    else:
        return redirect('/')
    
@app.route('/user_settings')
def user_settings():
    return render_template('user_settings.html')

@app.route('/logout')
def logout():
    session['authenticated'] = False
    return redirect('/')
            
        
    