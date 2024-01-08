#!/usr/bin/python3
"""
Module is used to output the json of the flask task
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON response with status 'OK'."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrieve the number of each object type."""
    objects_count = {
        'Amenity': storage.count('Amenity'),
        'City': storage.count('City'),
        'Place': storage.count('Place'),
        'Review': storage.count('Review'),
        'State': storage.count('State'),
        'User': storage.count('User')
    }

    return jsonify(objects_count)


if __name__ == '__main__':
    pass
