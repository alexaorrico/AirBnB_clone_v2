#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns JSON """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ Returns the number of each instance type """
    return jsonify(amenities=storage.count("47"),
                   cities=storage.count("36"),
                   places=storage.count("154"),
                   reviews=storage.count("718"),
                   states=storage.count("27"),
                   users=storage.count("31"))
