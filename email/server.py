from flask import Flask, render_template, redirect, session, request, flash
from mysqconnection import MySQLConnector

app = Flask(__name__)

app.secret_key = "anyKey"
db = MySQLConnector(app, 'Email_DB')

# the "re" module will let us perform some regular expression operations
import re
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# ============================index =================================

@app.route('/')
def index():
    #========load data ==========
    query = 'SELECT * FROM email'
    emails_list = db.query_db(query)
    return render_template('index.html')



# ============================ Add =================================
@app.route('/show' ,methods=['POST'])
def create():
    errors = False

    # define validations
    message="The email address you entered("+request.form['email_address']+") is a valid email address, THANK YOU !"
    if len(request.form['email_address']) < 1:
        flash("Email cannot be blank!")
        errors = True
    elif not EMAIL_REGEX.match(request.form['email_address']):
        flash("Invalid Email Address!")
        errors = True
    
       

    if errors == True:
        return redirect('/')
    else:
        # MAKE SURE EMAIL IS UNIQUE
        insert_query = "INSERT INTO email (email, created_at) VALUES(:email, NOW())"
        form_data = {
        "email": request.form['email_address'],
        }
        db.query_db(insert_query, form_data)

    #========load data ==========
    query = 'SELECT * FROM email'
    emails_list = db.query_db(query)
    return render_template('show.html', emails= emails_list , message=message)


# ============================ Delete Data =================================

@app.route('/<email_id>/delete', methods=["POST"])
def destroy(email_id):
    message="The email address is deleted !"

    # processing delete form
    delete_query = "DELETE FROM email WHERE id=:email_id"
    data = {
        "email_id": email_id
    }
    db.query_db(delete_query, data)
    #========load data ==========
    query = 'SELECT * FROM email'
    emails_list = db.query_db(query)
    return render_template('show.html', emails= emails_list , message=message)

app.run(debug=True)