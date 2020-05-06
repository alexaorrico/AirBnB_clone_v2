#!/usr/bin/python3
""" Api """

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
@app_views.route('/api/v1/status', methods=['GET'], strict_slashes=False)

def return_jason():
    """ return json status"""
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def class_status():
    """ endpoint that retrieves the number of each objects by type"""
    class_data = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(class_data)
