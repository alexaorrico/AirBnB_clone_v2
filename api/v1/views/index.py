#!/usr/bin/python3
""" ssss """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ sss """
    app_views = {'status': 'OK'}
    return app_views