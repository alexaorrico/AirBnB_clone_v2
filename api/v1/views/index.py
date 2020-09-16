#!/usr/bin/python3
""" index file """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """ Return http status response """
    return jsonify({'status': 'OK'})
