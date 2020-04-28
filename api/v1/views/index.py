#!/usr/bin/python3
"""views index"""

from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def stat():
    """return status code 200"""
    app_views = {'status': 'OK'}
    return jsonify(app_views), 200
