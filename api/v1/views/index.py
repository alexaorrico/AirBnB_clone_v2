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


classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status')
def status():
    """ Status Route Method """
    api_status = {"status": "OK"}
    return jsonify(api_status)


@app_views.route('/stats')
def stats():
    """Stats route methods"""
    info_dict = {}
    for key, value in classes.items():
        info_dict.update({key: storage.count(value)})
    return jsonify(info_dict)
