#!/usr/bin/python3
"""
    Index view of views module
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """
        Returns status
    """
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def stuff():
    '''Count By Class and Return JSON'''
    return jsonify({'states': storage.count('State'),
                    'users': storage.count('User'),
                    'amenities': storage.count('Amenity'),
                    'cities': storage.count('City'),
                    'places': storage.count('Place'),
                    'reviews': storage.count('Review'),
                    })
