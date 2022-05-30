#!/usr/bin/python3
"""Create an index"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """
    -----------------
    Return the status
    -----------------
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    -----------------
    Call count method
    -----------------
    """
    from models import storage
    from models.amenity import Amenity
    # from models.base_model import BaseModel, Base
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    classes = {"Amenity": Amenity, "City": City,
               "Place": Place, "Review": Review, "State": State, "User": User}

    result = {}
    for name, cls in classes.items():
        size = storage.count(cls)
        result.update({name: size})

    return jsonify(result)


@app_views.app_errorhandler(404)  # Because it has the blueprint.
def nop(error):
    """
    ----------------
    Return a 404 msg
    ----------------
    """
    return jsonify({'error': 'Not found'}), 404
