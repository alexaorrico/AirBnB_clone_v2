#!/usr/bin/python3
""" tbc """
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from flask import jsonify

@app_views.route('/status')
def index():
    """ tbc """
    return jsonify({
        "status": "OK"
        })

@app_views.route('/stats')
def stats():
    classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}
    obj_count = {}
    for item in classes:
        count = storage.count(classes[item])
        obj_count.update({item: count})
    return jsonify(obj_count)
