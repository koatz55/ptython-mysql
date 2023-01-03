from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.ninja import Ninjas
from flask_app.models.dojo import Dojos


@app.route('/create',methods=['POST'])
def create():
    data = {
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "age" :request.form['age'],
        "dojo_id": request.form['dojo_id'],
    }
    Ninjas.save(data)
    return redirect('/')


@app.route('/ninjas')
def ninjas():
    return render_template("all_ninjas.html",all_ninjas=Ninjas.get_all())


@app.route('/show/<int:ninja_id>')
def detail_page(ninja_id):
    data = {
        'id': ninja_id
    }
    return render_template("details_page.html",ninja=Ninjas.get_one(data))

@app.route('/update_ninja/<int:ninja_id>')
def edit_page(ninja_id):
    data = {
        'id': ninja_id
    }
    return render_template("update_ninja.html", ninja = Ninjas.get_one(data),all_dojos = Dojos.get_all(),)

@app.route('/update/<int:ninja_id>/', methods=['POST'])
def update(ninja_id):
    data = {
        'id': ninja_id,
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "age" :request.form['age'],
        "dojo_id": request.form['dojo_id'],
    }
    Ninjas.update(data)
    dojo = request.form['dojo_id'] 
    session[dojo] = dojo
    return redirect(f"/dojo/{int(dojo)}")

@app.route('/delete/<int:ninja_id>/<int:dojo_id>')
def deleteNinja(ninja_id,dojo_id):
    data = {
        'id': ninja_id,
        "dojo_id": dojo_id
    }
    Ninjas.destroy(data)
    return redirect(f'/dojo/{dojo_id}')

