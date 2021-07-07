#!/usr/bin/python3
"""
    View
"""
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def status():
    """ status route """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """ status route """
    from models import storage
    stats = dict()
    for k, c in classes.items():
        stats.update({k: storage.count(c)})
    return jsonify(stats)
