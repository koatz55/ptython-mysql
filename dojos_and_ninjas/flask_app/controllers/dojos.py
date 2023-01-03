from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.dojo import Dojos

@app.route('/newNinja')
def index():
    return render_template("create_ninja.html",all_dojos = Dojos.get_all())

@app.route('/dojo')
def get_Dojos():
    return render_template("index.html",all_dojos = Dojos.get_all())

@app.route('/dojo/<int:id>')
def show_dojo(id):
    data = {
        "id": id
    }
    return render_template('show_dojo_and_ninjas.html', dojo=Dojos.get_one_with_ninjas(data))

@app.route('/')
def home():
    return redirect('/dojo')

@app.route('/create/dojo',methods=['POST'])
def create_dojo():
    Dojos.save(request.form)
    return redirect('/dojo')

@app.route('/delete/dojo/<int:id>')
def delete(id):
    data = {
        'id': id,
    }
    Dojos.destroy_Dojo(data)
    return redirect('/dojo')

@app.route('/edit/<int:id>')
def edit_dojo(id):
    data = {
        'id': id,
    }
    return render_template('update_dojo.html', dojo = Dojos.get_one_with_ninjas(data), all_dojos = Dojos.get_all())

@app.route('/update_dojo/<int:id>', methods=['POST'])
def update_dojo(id):
    data = {
        'id': id,
        'name': request.form['name']
    }
    Dojos.update_dojo(data)
    return redirect('/')