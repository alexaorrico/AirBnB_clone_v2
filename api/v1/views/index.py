#!/usr/bin/python3
""" Index view for the API """
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def get_status():
    """Gets the status of the API"""
    return jsonify(status='OK')


@app_views.route('/stats')
def statistics():
    """Retuens the number of objects in storage"""
    stats = storage.count()
    response_body = jsonify(stats)
    status_code = 200
    return response_body, status_code
