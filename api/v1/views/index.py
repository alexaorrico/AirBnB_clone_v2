#!/usr/bin/python3
"""the main server api endpoint"""
from flask import Flask, redirect, Request, jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from api.v1.views import app_views
from api.v1.views.cities import cities


@app_views.route('/stats', methods = ['GET'], strict_slashs=True)
def status_report():
    """report the status of the api"""
    status_dict = {
        "amenities": storage.count(Amenity), 
        "cities": storage.count(City), 
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(status_dict)

@app_views.route('/status')
def get_status():
    """Get the status"""
    status = jsonify({
        "status": "OK"
    })
    status.status_code = 200
    return status
