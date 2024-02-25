#!/usr/bin/python3
""" index"""

from api.v1.views import app_views

@app_views.route('/status', methods='(get'))
def status():
    return jsonify ({'ststus: OK'})
