#!/usr/bin/python3
"""This file returns the JSON status ok"""

from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def index():
    return jsonify({"status": "OK"})
