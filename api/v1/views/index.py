#!/usr/bin/python3
""" AirBnB v3 flask Api v1: index.py """

from models import storage
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Api status route"""
    return '{"status": "OK"}'
