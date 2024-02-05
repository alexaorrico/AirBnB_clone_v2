#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
import storage
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

@app_views.route('/status')
def get_status():
    """returns a JSON: "status": 'OK'"""
    rep = {"status": "OK"}

    return jsonify(rep)

@app_views.route('/api/v1/stats')
def nub_obj():
    """Create an endpoint that retrieves the number of each objects"""
    dictt = {}
    lista = [State, City, User, Place, Review, Amenity]

    for clase in lista:
        count = storage.count(clase)
        dictt[clase.__name__] = count
    return jsonify(dictt)
