from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.vehicle_model import Vehicle
from flask_app.models.favourite_model import Favourite
from flask_app.models.bid_model import Bid
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
@app.route('/show/vehicle/<int:vehicle_id>')
def show_vehicle(vehicle_id):
    vehicle=Vehicle.get_one_by_id({'id':vehicle_id})
    favourites=Favourite.get_one_by_id({'vehicle_id':vehicle_id,'user_id': session['user_id'] })
    last_bid=Bid.get_last_bid_by_vehicle_id({'vehicle_id':vehicle_id})
    return render_template('vehicle.html',vehicle=vehicle,favourites=favourites,last_bid=last_bid)

@app.route('/show/result')
def show_result():
    all_vehicles = Vehicle.get_result()
    vehicles=Vehicle.get_all()
    return render_template('results.html',all_vehicles=all_vehicles,vehicles=vehicles)
