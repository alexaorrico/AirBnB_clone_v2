#!/usr/bin/python3
# import api.v1.views
from flask import Flask
from api.v1.views import app_views
from json import dumps, loads
from models import storage


@app_views.route('/status')
def status():
    """returns status ok"""
    return (loads('{"status": "OK"}'))


@app_views.route('/stats')
def numtypes():
    dicty = {}
    amenC = storage.count("Amenities")
    dicty["amenities"] = amenC
    cityC = storage.count("City")
    dicty["cities"] = cityC
    placeC = storage.count("Places")
    dicty["places"] = placeC
    reviewC = storage.count("Review")
    dicty["reviews"] = reviewC
    stateC = storage.count("State")
    dicty["states"] = stateC
    userC = storage.count("User")
    dicty["users"] = userC

    return loads(dumps(dicty))
