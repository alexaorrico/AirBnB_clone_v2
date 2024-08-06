#!/usr/bin/python3
"""
create Flask app; app_views
"""

from flask import  jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def api_status ():
    reaponse = ('status': OK)
    return jsonify(response)


@app_views.route('/stats', methods=["GET"], strict_slashes=False)
def stats():
    """
    Retrieves the number of each objects by type
    """

stats = {
        'Amenity': storage.count('Amenity'),
        'City': storage.count('City'),
        'Place': storage.count('Place'), 
        'Review': storage.count('Review'),
        'State': storage.count('State'),
        'User': storage.count('User')
}


return jsonify(stats)
