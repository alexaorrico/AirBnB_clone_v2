#!/usr/bin/python3
"""JSON OK status will return"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City, "places": Place,
        "reviews": Review, "states": State, "users": User}

@app_views.route('/status', strict_slashes=False)
def status():
    """Return JSON status ok"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Return JSON count stats"""
    n_dict = {}
    for key, value in classes.items():
        n_dict[key] = storage.count(value)
    return jsonify(n_dict)

if __name__ == "__main__":
    pass
