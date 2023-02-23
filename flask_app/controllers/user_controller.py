from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user_model import User
from flask_app.models.vehicle_model import Vehicle
# ============= display route =============
@app.route('/')
def user():
    return render_template('registration.html')
# ============= action route =============
@app.route('/register', methods=['post'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    data={
        **request.form,
        'password':bcrypt.generate_password_hash(request.form['password'])
    }
    user=User.register(data)
    session['user_id']=user

    return redirect('/')
# ============= display route =============
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/')
    user= User.get_by_id({'id': session['user_id']})
    return render_template("home.html",user=user)
    
# ============= action route =============
@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password","email")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/home')

    # ============= action route =============
@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')