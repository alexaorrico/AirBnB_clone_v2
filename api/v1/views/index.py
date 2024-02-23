#!/usr/bin/python3
""" this responds with a message """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})
