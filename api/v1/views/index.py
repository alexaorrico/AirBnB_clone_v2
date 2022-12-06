#!/usr/bin/python3
"""Index"""


from api.v1.views import app_views
import json
from models import storage


@app_views.route('/status')
def status():
    return {"status": "ok"}


@app_views.route('/stats')
def stats():
    return {"aminities": storage.count('Amenity'),
            "cities": storage.count('City'),
            "places": storage.count('Place'),
            "reviews": storage.count('Review'),
            "states": storage.count('State'),
            "users": storage.count('User')}
