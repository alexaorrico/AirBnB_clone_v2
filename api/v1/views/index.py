#!/usr/bin/python3
'''index page for the status of api'''


from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


classes = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def status():
    '''return status'''
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    my_list = {}
    for key, value in classes.items():
        num = storage.count(value)
        my_list[key] = num
    return jsonify(my_list)


if __name__ == "__main__":
    pass
