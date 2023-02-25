from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user_model import User
from flask_app.models.vehicle_model import Vehicle

# ============= display route =============
@app.route('/registration')
def user():
    if 'user_id' in session:
        return redirect('/')
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
@app.route('/')
def home():
    return render_template("home.html")
    
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
    return redirect('/')

    # ============= action route =============
@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')
    # ============= action route =============
@app.route('/favorize/vehicle',methods=['POST'])
def favourite_vehicle():
    data = {
        'user_id': request.form['user_id'],
        'vehicle_id': request.form['vehicle_id']
    }
    User.add_favorite(data)
    
    return redirect(f"/show/vehicle/{request.form['vehicle_id']}")
@app.route('/unfavorize/vehicle',methods=['POST'])
def unfavorize_vehicle():
    data = {
        'user_id': session['user_id'],
        'vehicle_id': request.form['vehicle_id']
    }
    User.remove_favorite(data)
    
    return redirect(f"/show/vehicle/{request.form['vehicle_id']}")