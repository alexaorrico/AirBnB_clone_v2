#!/usr/bin/pyhton
""" Index of several Class for JSON API """
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def Status():
    return jsonify(status='ok')
