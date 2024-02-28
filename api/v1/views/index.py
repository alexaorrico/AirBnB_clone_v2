#!/usr/bin/python3
""" The index package"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """ Returns a JSON with status OK """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def endpoint():
    """ Retrieves the number of each """
