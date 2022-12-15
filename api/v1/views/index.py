#!/usr/bin/python3
""" first route """

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_route():
    """ Route that returns a JSON """
    return jsonify({'status': 'OK'})
