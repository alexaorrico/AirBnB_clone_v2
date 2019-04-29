#!/usr/bin/python3
"""index file, main view file
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def service_status():
    """returns the status of the RESTful service"""
    """ TODO check if this formatting is okay for json response with
        holberton checker """
    return jsonify({'status': 'OK'})
