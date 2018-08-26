from flask import Flask, render_template, redirect, session, request, flash
from mysqconnection import MySQLConnector

app = Flask(__name__)

app.secret_key = "anyKey"
db = MySQLConnector(app, 'users_db')

# the "re" module will let us perform some regular expression operations
import re
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
CHAR_REGEX = re.compile(r'^[0-9.+_-]+$')

import md5 # imports the md5 module to generate a hash

# ============================index =================================

@app.route('/')
def index():
    user_query ="SELECT * FROM users"
    users = db.query_db(user_query)
    return render_template('index.html',users=users)

# ============================ add =================================
@app.route('/add')
def add():
    return render_template('add.html')

# ============================ Add Process =================================
@app.route('/add_user', methods=['POST'])
def add_user():
    errors = False 

 # define validations
    if len(request.form['email']) <1 :
        flash("* Email cannot be black !")
        errors = True
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("* Invalid Email Address!")
        errors = True

    # if len(request.form['password']) <8 :
    #     flash("* password - at least 8 characters !")
    #     errors = True
    # elif not request.form['password'] == request.form['re-password']:
    #     flash("* password & re-type password is not matched!")
    #     errors = True

    
    if len(request.form['first_name']) <3 :
        flash("* Invalid First Name - at least 2 characters")
        errors = True
    if CHAR_REGEX.match(request.form['first_name']):
        flash("* Invalid First Name -  letters only")
        errors = True
    if len(request.form['last_name']) <3 :
        flash("* Invalid Last Name - at least 2 characters")
        errors = True
    if CHAR_REGEX.match(request.form['last_name']):
        flash("* Invalid Last Name -  letters only")
        errors = True

    if errors == True:
        return redirect('/add')
    else:

        #========load data ==========
        query = 'SELECT * FROM users where email=:email'
        data ={
            "email":request.form['email']
        }
        user = db.query_db(query,data)
        if len(user)>0 :
            flash('* This E-mail is existed ')
            return redirect('/add')
        else:
            insert_query = "INSERT INTO users (email,first_name,last_name,created_at) VALUES(:email,:first_name,:last_name, NOW())"
            form_data = {
            "email": request.form['email'],
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name']
            }
            db.query_db(insert_query, form_data)
            return redirect('/')

# ============================Edit =================================

@app.route('/<user_id>/edit')
def edit(user_id):
    user_query = "SELECT * FROM users where id=:id"
    data ={
        "id": user_id,
    }
    users = db.query_db(user_query,data)
    return render_template('edit.html',user=users[0])




# ============================ Edit Process =================================
@app.route('/edit_user', methods=['POST'])
def edit_user():
    errors = False 

 # define validations
    if len(request.form['email']) <1 :
        flash("* Email cannot be black !")
        errors = True
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("* Invalid Email Address!")
        errors = True

    # if len(request.form['password']) <8 :
    #     flash("* password - at least 8 characters !")
    #     errors = True
    # elif not request.form['password'] == request.form['re-password']:
    #     flash("* password & re-type password is not matched!")
    #     errors = True

    
    if len(request.form['first_name']) <3 :
        flash("* Invalid First Name - at least 2 characters")
        errors = True
    if CHAR_REGEX.match(request.form['first_name']):
        flash("* Invalid First Name -  letters only")
        errors = True
    if len(request.form['last_name']) <3 :
        flash("* Invalid Last Name - at least 2 characters")
        errors = True
    if CHAR_REGEX.match(request.form['last_name']):
        flash("* Invalid Last Name -  letters only")
        errors = True

    if errors == True:
        return redirect('/add')
    else:

        #========load data ==========
        query = "UPDATE users SET first_name=:first_name, last_name=:last_name, email=:email WHERE id=:id"
        data ={
            "email":request.form['email'],
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "id": request.form['id']
        }
        db.query_db(query,data)

        return redirect('/')

# ============================ show =================================

@app.route('/<user_id>/show')
def show(user_id):
    user_query = "SELECT * FROM users where id=:id"
    data ={
        "id": user_id,
    }
    users = db.query_db(user_query,data)
    return render_template('show.html',user=users[0])



# ============================ Delete =================================

@app.route('/<user_id>/delete', methods=['POST'])
def destroy(user_id):
    # processing delete form
    delete_query = "DELETE FROM users WHERE id=:id"
    data = {
        "id": user_id
    }
    print "===============================  "
    print delete_query
    db.query_db(delete_query, data)
    message="User id [ " + user_id +" ] is deleted sucessfully !"
    flash(message)
    return redirect('/')

# ============[ End ]=========================

app.run(debug=True)