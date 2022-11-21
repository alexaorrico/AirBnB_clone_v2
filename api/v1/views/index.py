#!/usr/bin/ python3
"""
Creates a status route
"""


from flask import jsonify
from api.v1 import views

my_app = views.app_views


@my_app.route('/status')
def getStatus():
    return jsonify({"status": "OK"})
