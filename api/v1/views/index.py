#!/usr/bin/python3
""" 
    module index 
"""

from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', methods=['GET'])
def statCode():
    """ 
        a function that return a json string
    """
    js  = {'status': 'OK'}
    return jsonify(js)
