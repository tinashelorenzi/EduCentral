from flask import Flask, render_template, request, redirect, session, jsonify
import os, sqlite3
from handlers import login_handler,cipherguard, database_handler

from cs50 import SQL
app = Flask(__name__)
app.debug = True
enckey = "95fb144ffdb4a1899ce187a015ec02a21a227018"
app.secret_key = 'Shall I compare thee to a summers day'
adminallowed = ['admin','reception']

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
            
@app.route('/register_learner') 
def register_learner():
    userstatus = database_handler.getuserstatus(session['userid'])
    if userstatus in adminallowed:
        return render_template('register.html')
    else:
        return 'Not allowed to view this region'

@app.route('/parents_database')
def parents_database():
    userstatus = database_handler.getuserstatus(session['userid'])
    if not session.get('authenticated'):
        return redirect('/')  
    if userstatus in adminallowed:
        parents = database_handler.get_parents()
        id = session.get('userid')
        username = database_handler.if_fetch_name(id)
        return render_template('database_parents.html', parents=parents,username=username)
    else:
        return 'Not allowed to view this region'
    
@app.route("/submit_studentreg",methods=["GET", "POST"])
def student_review():
    userstatus = database_handler.getuserstatus(session['userid'])
    if userstatus in adminallowed:
        if request.method == "GET":
            return redirect('/register_learner')
        name = request.form["name"]
        surname = request.form["surname"]
        dob = request.form["date_of_birth"]
        address = request.form["address"]
        idnr = request.form["idnr"]
        grade = request.form["grade"]
        parentidnr = request.form["parentidnr"]
        Parentname = request.form["Parentname"]
        Parentsurname = request.form["Parentsurname"]
        monthlyfee = request.form["monthlyfee"]
        allergies = request.form["allergies"]
        Ename = request.form["Ename"]
        Etel = request.form["Etel"]
        econditions = request.form["emergency-conditions"]
        dietres = request.form["dietres"]
        langs = request.form["langs"]
        pschool = request.form["pschool"]
        reasprev = request.form["reasprev"]
        snotes = request.form["snotes"]
        sports = request.form["sports"]
        parentemail = request.form["parentemail"]
        parenttel = request.form["parenttel"]
        medicine = request.form["med"]
        image_file = request.files['image']
        gender = request.form["gender"]
        new_file_name = idnr
        new_file_path = os.path.join('uploads/', new_file_name)
        image_file.save(new_file_path)
        
        #Create parent first
        database_handler.submit_parent(parentidnr,Parentname,Parentsurname,parenttel,parentemail,address)
        
        #Push to review
        database_handler.submit_review(name,surname,dob,address,parentidnr,grade,monthlyfee,allergies,
                  sports,idnr,Ename,Etel,
                  econditions,medicine,dietres,langs,
                  pschool,reasprev,snotes,gender)
        return redirect('/register_learner')
    else:
        return redirect('/')
    
@app.route('/review_students')
def rev_students():
    userstatus = database_handler.getuserstatus(session['userid'])
    if not session.get('authenticated'):
        return redirect('/') 
    if userstatus in adminallowed:
        registrations = database_handler.get_student_reviews()
        return render_template('review_registrations.html', applications=registrations)
@app.route('/decline',methods=["POST"])
def decline_student():
        if not session.get('authenticated'):
            return redirect('/') 
        if request.method == 'POST':
            applicant_id = request.form['student_id']

        # Connect to the SQLite database
            conn = sqlite3.connect('database/student_data.db')
            cursor = conn.cursor()

        # Delete the password by its ID
            query = "DELETE FROM student_review WHERE id = ?"
            cursor.execute(query, (applicant_id,))

        # Commit the changes and close the connection
            conn.commit()
            conn.close()

        # Redirect back to the dashboard
        return redirect('/review_students')
    

if __name__ == "__main__":
    app.run(debug=True, port=4444)