from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():

    return render_template('login/login.html')

@app.route('/register/user', methods = ['POST'])
def register_user():

    if User.validate_user(request.form):
        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email': request.form['email'],
            'password' : bcrypt.generate_password_hash(request.form['password'])
        }
        id = User.save(data)
        session['user_id'] = id
        return redirect('/user/home')
    else:
        return redirect('/')

@app.route('/user/home')
def user_home():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id' : session['user_id']
    }
    return render_template('user/user_home.html', user = User.get_by_id(data), sightings = Sighting.get_all() )

@app.route('/report/sighting')
def create_alert():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id': session['user_id']
    }

    return render_template('sighting/report.html', user = User.get_by_id(data))

@app.route('/user/info')
def show_user_info():
    if 'user_id' not in session:
        return redirect('/')
        
    data = {
        'id': session['user_id']
    }
    
    return render_template('user/user_info.html', user = User.get_by_id(data))



@app.route('/login', methods = ['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash('invalid credentials', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('invalid credentials', 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/user/home')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

