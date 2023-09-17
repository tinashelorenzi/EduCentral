from flask import Flask, render_template, request, redirect, session, jsonify
import os, sqlite3

from cs50 import SQL
app = Flask(__name__)
app.secret_key = 'Shall I compare thee to a summers day'

@app.route("/")
def index():
    if session.get('authenticated'):
        return redirect('dashboard')
    else:
        return render_template('login.html')

@app.route('/login')
def login():
    if request.method == "GET":
        return render_template("index.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        
    