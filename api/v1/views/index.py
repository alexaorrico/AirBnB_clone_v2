#!/usr/bin/python3
"""
create a route /status on the object app_views that returns a JSON
and an endpoint that retrieves the number of each objects by type
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.state import State
from models.user import User
from models.review import Review

classes = {"amenites": Amenity, "places": Place, "city": City,
           "state": State, "user": User, "review": Review}

@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

def get_stats():
    counts = {}
    for clss in classes:
        counts[clss] = storage.count(classes[clss])
    return jsonify(counts)
