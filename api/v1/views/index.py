#!/usr/bin/python3
"""run flask server"""
from api.v1.views import app_views


@app_views.route('/status')
def status_ok():
    return {'status': 'OK'}
