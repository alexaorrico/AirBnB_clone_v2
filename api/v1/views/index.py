#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status_api():
    status_api = 'OK'
    return jsonify({'status': status_api})


@app_views.route('/stats', strict_slashes=False)
def stats_api():
    return jsonify({
        'amenities': storage.count("Amenity"),
        'cities': storage.count("City"),
        'places': storage.count("Place"),
        'reviews': storage.count("Review"),
        'states': storage.count("State"),
        'users': storage.count("User")
    })
