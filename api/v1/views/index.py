#!/usr/bin/python3
""" API Status Route """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
}


@app_views.route('/status')
def status():
    """ Status Route Method """
    api_status = {"status": "OK"}
    return jsonify(api_status)


@app_views.route('/stats')
def stats():
    """Stats route methods"""
    info_dict = {key: storage.count(value) for key, value in classes.items()}
    return jsonify(info_dict)
