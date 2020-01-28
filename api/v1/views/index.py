#!/usr/bin/python3
"""
Index module
"""
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """return dictionary with status"""
    return {"status": "OK"}


@app_views.route('/stats')
def stats():
    """Retrieve number of each objects by type"""
    stat_dict = {}
    stat_dict["amenities"] = storage.count("Amenity")
    stat_dict["cities"] = storage.count("City")
    stat_dict["places"] = storage.count("Place")
    stat_dict["states"] = storage.count("State")
    stat_dict["users"] = storage.count("User")
    return stat_dict
