#!/usr/bin/python3
# This is the index page

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    # This returns a status on the api
    return jsonify(status='OK')
