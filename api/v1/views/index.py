#!/usr/bin/python3
''' blueprint routes '''
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    ''' return status '''

    return (jsonify({"status": "OK"}))
