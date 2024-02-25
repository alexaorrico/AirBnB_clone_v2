#!/usr/bin/python3
""" app_view Blueprint """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def show_status():
    """ Shows the api response status """
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def show_stats():
    """ Shows the number of each object """
    classes = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']
    class_count = {}
    for clas in classes:
        count = storage.count(clas)
        class_count[clas] = count
    return jsonify(class_count)
