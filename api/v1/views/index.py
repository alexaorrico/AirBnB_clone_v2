#!/usr/bin/python3
"""
Index module that creates routes on app_views objects.
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Returns OK status"""
    return jsonify({'status': 'OK'})
