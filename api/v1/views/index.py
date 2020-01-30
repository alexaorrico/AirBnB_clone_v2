#!/usr/bin/python3
"""
    index
"""
from flask import Flask
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def status():
    """ status """
    return {"status": "OK"}


@app_views.route("/stats")
def stats():
    """ stats """
    ret = {}

    def form(name):
        """ simple format (lowercase + plural) """
        name = name.lower()
        if name[-1] == 'y':
            name = name[:-1] + 'ie'
        return name + 's'
    for name in ["Amenity", "City", "Place", "Review", "State", "User"]:
        ret[form(name)] = storage.count(name)
    return ret
