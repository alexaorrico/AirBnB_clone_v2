#!/usr/bin/python3
"""
create flask app; app_views
"""
from api.v1.views import app_views
from flask import jasonify

@app_views.route('/status')
def api_status():
    """
    define api status
    """
    response = {'status': "OK"}
    return jasonify(response)

@app_views.route('/status')
def get_status():
    """
    
    """
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Reviews'),
        'states': storage.count('State'),
        'users': storage.count('User',)
    }