#!/usr/bin/python3
# Index
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}

@app_views.route('/states' methods=['GET'])
def states():
    """def function que devuelve una lista de todos los State"""
    if request.method == 'GET':
        states = storage.all(State)
        return jsonify(states)

    
