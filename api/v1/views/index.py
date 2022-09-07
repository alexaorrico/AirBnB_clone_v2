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
from flask import jsonify

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}

@app_views.route('/status')
def status():
    """def function que devuelve un json referenciando al status"""
    dictionary = {}
    dictionary['status'] = "Ok"
    return jsonify(dictionary)

@app_views.route('/stats')
def countype():
    """def function que devuelve un contador de objetos de cada clase"""
    dic = {}
    for key, value in classes.items():
        count = storage.count(value)
        dic[key] = count
    return jsonify(dic)