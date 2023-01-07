from flask import Flask
app = Flask(__name__)
app.secret_key = "My Secret Key! SHHHHH!"
from flask import render_template, redirect, request, session
# import the function that will return an instance of a connection
from mysqlconnection import connectToMySQL
# model the class after the users_schema table from our database
class user:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('users_schema').query_db(query)
        # Create an empty list to append our instances of users
        users = []
        # Iterate over the db results and create instances of users_schema with cls.
        for results in results:
            users.append( cls(results) )
        return users
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users_schema.users ( first_name , last_name , email , created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , NOW() , NOW() );"
        return connectToMySQL('users_schema').query_db( query, data )
    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('users_schema').query_db(query,data)
        return (results[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('users_schema').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('users_schema').query_db(query,data)



@app.route('/')
def home():
    return redirect('/all_users')

@app.route('/create')
def newuser():
    return render_template('index.html')

@app.route('/add_user', methods=["POST"])
def create_user():
    data = {
    'first_name': request.form['first_name'],
    "last_name" : request.form["last_name"], 
    "email" : request.form["email"]}
    user.save(data)
    return redirect('/all_users')

@app.route("/all_users")
def index():
    users = user.get_all()
    print(users)
    return render_template("all_crew.html", all_users = users)

@app.route("/user/edit/<int:id>")
def edit(id):
    data = {
        'id' : id,
    }
    return render_template("edit_user.html", user = user.get_one(data))

@app.route("/user/update/<int:id>", methods=["POST"])
def update(id):
    data = {
    'id' : id,
    'first_name': request.form['first_name'],
    "last_name" : request.form["last_name"], 
    "email" : request.form["email"]}
    user.update(data)
    print("updated")
    return redirect("/all_users")

@app.route('/user/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    user.destroy(data)
    return redirect('/')

@app.route("/user/view/<int:id>")
def view(id):
    data = {
        "id" : id
    }
    return render_template('pirateinfo.html', user = user.get_one(data))

if __name__ == "__main__":
    app.run(debug=True)