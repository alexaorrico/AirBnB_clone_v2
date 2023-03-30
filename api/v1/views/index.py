#!/usr/bin/python3
"""Route to index page"""
from json import dumps
from flask import Response
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return status of API"""
    return Response(dumps({"status": "OK"}), content_type='application/json')
