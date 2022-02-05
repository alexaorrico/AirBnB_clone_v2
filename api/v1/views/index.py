#!/usr/bin/python3
""" index routes """
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ Status ok """
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ hbnb stats """
    objects = {
        'amenities': 'Amenity',
        'cities': 'City',
        'places': 'Place',
        'reviews': 'Review',
        'states': 'State',
        'users': 'User'
    }
    processed_stats = {key: storage.count(value)
                       for key, value in objects.items()}
    return jsonify(processed_stats), 200


if __name__ == '__main__':
    pass
