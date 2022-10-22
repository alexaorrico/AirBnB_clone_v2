#!/usr/bin/python3
""" index module showing the status endpoint """
import json
from models import storage

from api.v1.views import app_views


@app_views.route('/status')
def show_status():
    return json.dumps({"status": "OK"})

@app_views.route('/api/v1/stats')
def show_count():
    new_dict = {
        "amenities": storage.count("Amenities"),
        "cities": storage.count("Cities"),
        "places": storage.count("Places"),
        "reviews": storage.count("Reviews"),
        "states": storage.count("States"),
        "users": storage.count("Users")
    }
    return json.dumps(new_dict)