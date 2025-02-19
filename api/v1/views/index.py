#!/usr/bin/python3
""" Blueprint Views
"""
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage


@app_views.route('/status')
def status():
    """ Returns status of request
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """ Returns the number of items in storage
    """
    return jsonify(storage.count())
