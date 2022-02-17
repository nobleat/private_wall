from flask_app import app
from flask import render_template, redirect,session,request, flash
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/register', methods=['POST'])
def register():
    if User.validate(request.form) ==False:
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash
        }
    user_id=User.save(data)
    session['user.id']=user_id
    return render_template('wall.html', user=User.get_by_email(data))

@app.route("/login", methods=['post'])
def log_in():
    data={'email': request.form['email']}
    userdb = User.get_by_email(data)
    if not userdb:
        flash ("Invalid Email or Password")
        return redirect('/')
    if not bcrypt.check_password_hash(userdb.password, request.form['password']):
        flash ("Invalid Email or Password")
        return redirect ('/')
    session['user_id']=userdb.id
    return redirect('/home')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    messages = Message.get_msgs(data)
    users = User.get_all()
    return render_template("wall.html",user=user, messages=messages, users= users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')