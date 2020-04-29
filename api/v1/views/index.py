#!/usr/bin/python3
""" show status """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ object app_views that returns a JSON """
    app_views = {'status': 'OK'}
    return jsonify(app_views)
