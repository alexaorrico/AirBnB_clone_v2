#!/usr/bin/python3
"""file index"""
from models.amenity import Amenity
from api.v1.views import app_views
from models.city import City
from flask import jsonify
from models.place import Place
from models.review import Review
from models.state import State
from models import storage
from models.user import User


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def status():
    """def function que devuelve un json referenciando al status"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def countype():
    """def function que devuelve un contador de objetos de cada clase"""
    dic = {}
    for key, value in classes.items():
        count = storage.count(value)
        dic[key] = count
    return jsonify(dic)
