#!/usr/bin/python3
"""Index module"""
from flask import jsonify
from models import storage
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from api.v1.views import app_views


classes = {"amenity": Amenity, "city": City,
           "place": Place, "review": Review, "state": State, "user": User}


@app_views.route('/status', strict_slashes=False)
def status():
    """ returns a JSON: "status" """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """endpoint that retrieves the number of each objects by type
    """
    new_dict = {}
    for key, value in classes.items():
        new_dict[key] = storage.count(value)
    return jsonify(new_dict)


if __name__ == "__main__":
    pass
