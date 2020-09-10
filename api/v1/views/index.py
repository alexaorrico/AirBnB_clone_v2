#!/usr/bin/python3
""" flask api root routes module """
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

classes = [Amenity, City, Place, Review, State, User]


@app_views.route('/status', strict_slashes=False)
def status():
    """ it retrieve the page status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ It retrieve the current stats of the elements
    into the data_base """
    stats = {}
    for clss in classes:
        name = clss.__tablename__
        stats[name] = storage.count(clss)
    return stats
