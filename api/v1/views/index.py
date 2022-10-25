#!/usr/bin/python3
"""default route"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models import storage
from models.user import User


@app_views.route('/status')
def status():
    return jsonify({
            "status": "OK"
        })


@app_views.route('/stats', methods=["GET"])
def count():
    all_cls = {
               "amenities": Amenity,
               "cities": City,
               "places": Place,
               "reviews": Review,
               "states": State,
               "users": User
              }
    all_count = {}
    for i, j in all_cls.items():
        all_count[i] = storage.count(j)
    return jsonify(all_count)
