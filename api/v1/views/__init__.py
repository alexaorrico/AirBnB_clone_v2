#!/usr/bin/python3
"""
initialize Blueprint
"""

from flask import Blueprint


app_views = Blueprint("mold", __name__, url_prefix='/api/v1')


@app_views.route('/api/v1')
def api_vi_route():
    """ print returns a JSON: "status": "OK" """
    
