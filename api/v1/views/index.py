#!/usr/bin/python3
""" doc for index.py """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """ doc for status method """
    return jsonify({"status": "OK"})


