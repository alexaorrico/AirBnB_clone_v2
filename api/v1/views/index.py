#!/usr/bin/python3
""" Main route """

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
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
           "users": User,
           }


@app_views.route('/status')
def status_check():
    '''
    checks status of JSON
    '''
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def obj_count():
    '''
    retrieves number of objects by type
    '''
    obj_count = {}
    for key, value in classes.items():
        obj_count[key] = storage.count(value)
    return jsonify(obj_count)


if __name__ == '__main__':
    pass
