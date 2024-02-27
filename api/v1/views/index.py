#!/usr/bin/python3
"""
Module for giving info on application status
"""
#importing the important modules
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, Blueprint, render_template, abort
from models import storage
from models.review import Review


@app_views.route('/status', methods=['GET'])
def status_report():
    """
    function that permits us view status report
    """
    return (jsonify({"status": "OK"}))


@app_views.route('/stats', methods=['GET'])
def stats_report():
    """
    This function enables us to view stats concerning our site
    """
    return (jsonify({"amenities": storage.count(Amenity),
                     "cities": storage.count(City),
                     "places": storage.count(Place),
                     "reviews": storage.count(Review),
                     "states": storage.count(State),
                     "users": storage.count(User)}))
