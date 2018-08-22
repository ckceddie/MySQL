from flask import Flask , redirect, Response,session ,render_template,request
app=Flask(__name__)

app.secret_key = "a;dfksjladwfopahwefhjkl;"

from mysqlconnection import MySQLConnector
mysql = MySQLConnector(app,'myFriend')


# ============================index =================================
@app.route("/")
def index():
    query = "SELECT * FROM profile"                           # define your query
    friends = mysql.query_db(query)                           # run query with query_db()
    return render_template('index.html', all_friends=friends) # pass data to our template



# ============================Add New =================================
@app.route('/friends', methods=['POST'])
def create():
    # Write query as a string. Notice how we have multiple values
    # we want to insert into our query.
    query = "INSERT INTO profile (first_name, last_name, occupation , created_at,updated_at) VALUES (:first_name, :last_name, :occupation , NOW(), NOW() )"
    # We'll then create a dictionary of data from the POST data received.
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'occupation': request.form['occupation']
           }
    # Run query, with dictionary values injected into the query.
    mysql.query_db(query, data)
    return redirect('/')

# ============================ Show Data =================================

@app.route('/<friend_id>')
def show(friend_id):
    # Write query to select specific user by id. At every point where
    # we want to insert data, we write ":" and variable name.
    query = "SELECT * FROM profile WHERE id = :id"
    # Then define a dictionary with key that matches :variable_name in query.
    data = {'id': friend_id}
    # Run query with inserted data.
    friend = mysql.query_db(query, data)
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias one_friend.
    return render_template('show.html', friend=friend[0])

# ============================redirect blank page for New =================================

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/<friend_id>/edit')
def edit(friend_id):
    friend_query = 'SELECT * FROM profile WHERE id=:friend_id'
    data = {
        'friend_id': friend_id
    }
    friends_list = mysql.query_db(friend_query, data)
    friend = friends_list[0]
    return render_template('edit.html', friend=friend)


# ============================ Update Data=================================


@app.route("/<friend_id>/update",methods=["POST"])
def update(friend_id):
    
  # processing the update form
    update_query = "UPDATE profile SET first_name=:first_name, last_name=:last_name, occupation=:occupation, updated_at=NOW() WHERE id=:friend_id"
    form_data = {
      "first_name": request.form['first_name'],
      "last_name": request.form['last_name'],
      "occupation": request.form['occupation'],
      "friend_id": friend_id
    }
    mysql.query_db(update_query, form_data)
    return redirect('/')

# ============================ Delete =================================

@app.route('/<friend_id>/delete', methods=["POST"])
def destroy(friend_id):
    # processing delete form
    print "======================%S===================",friend_id
    delete_query = "DELETE FROM profile WHERE id=:friend_id"
    data = {
        "friend_id": friend_id
    }
    mysql.query_db(delete_query, data)
    return redirect('/')


app.run(debug=True)