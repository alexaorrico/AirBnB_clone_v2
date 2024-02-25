#!/usr/bin/python3
""" app_view Blueprint """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def show_status():
    """ Shows the api response status """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def show_stats():
    """ Shows the number of each class objects """
    classes = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']
    class_count = {}
    for clas in classes:
        class_count[clas] = storage.count(clas)
    return jsonify(class_count)
