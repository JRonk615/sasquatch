from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.sighting import Sighting

@app.route('/create/sighting', methods =['POST'])
def create_sighting():
    if 'user_id' not in session:
        return redirect('/')
    
    if not Sighting.save(request.form):
        return redirect('/report/sighting')
    
    else:
        return redirect('/user/home')
@app.route('/delete/sighting/<int:id>')
def delete_sighting(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id' : id
    }

    Sighting.delete_sighiting(data)
    return redirect('/user/home')

@app.route('/edit/sighting/<int:id>')
def edit_sighting(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id' : id
    }
    user = {
        'id': session['user_id']
    }

    return render_template('sighting/edit_sighting.html', sighting = Sighting.get_by_id(data), user = User.get_by_id(user))

@app.route('/update/sighting/<int:id>', methods = ['POST'])
def update_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Sighting.validate_sighting(request.form):
        return redirect(f'/edit/sighting/{id}')

    data = {
        'id' : id,
        'location' : request.form['location'],
        'what_happened' : request.form['what_happened'],
        'date_of' : request.form['date_of'],
        'count' : request.form['count'],
    
    }
    Sighting.update(data)
    return redirect('/user/home')

@app.route('/view/sighting/<int:id>')
def view_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
        
    data = {
        'id' : id,
    }
    user = {
        'id': session['user_id']
    }
    return render_template('sighting/view_sighting.html', sighting = Sighting.get_by_id(data), user = User.get_by_id(user))