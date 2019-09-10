#!/usr/bin/python3
''' index.py to connect to API '''
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def hbnbStatus():
    ''' hbnb Status '''
    return jsonify({"status": "OK"})
