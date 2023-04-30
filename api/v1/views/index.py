#!/usr/bin/python3
"""Contain our APIs"""
from api.v1.views import app_views
import json

@app_views.route('/status')
def status():
    return json.dumps({'status': 'OK'})
