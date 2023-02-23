from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.vehicle_model import Vehicle
#=============DISPLAY ROUTE==============================
@app.route('/vehicle/new')
def new_vehicle():
    if 'user_id' not in session :#=================bch tekml problem BD(and usere.role)==============
        return redirect('/')
    return render_template('add_vehicle.html')
#============================ACTION ROUTE================================
@app.route('/vehicles/add', methods=['POST'])
def add_vehicle():
    if not Vehicle.validate_vehicle(request.form):
        return redirect('/vehicle/new')
    data = {
        **request.form,
        'user_id': session['user_id']#=================bch tekml problem BD(and usere.role)==============
    }
    Vehicle.save_vehicle(data)
    return redirect('/')
""" @app.route('/show/vehicle/<int:id>')
def new_vehicle(id):
    return(render_template('vehicle.html')) """
@app.route('/show/result')
def show_result():
    all_vehicles = Vehicle.get_result()
    vehicles=Vehicle.get_all()
    return render_template('results.html',all_vehicles=all_vehicles,vehicles=vehicles)
