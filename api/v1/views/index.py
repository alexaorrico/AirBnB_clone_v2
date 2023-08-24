"""Module that have the route of app_views"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def hbnbstatus():
    """function that return json on status route"""
    return jsonify({'status': "OK"})
