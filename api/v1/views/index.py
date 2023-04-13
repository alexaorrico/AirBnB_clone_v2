#!/usr/bin/python3
'''
    return json
'''


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models import amenity, city, place, review, state, user


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def retrieve_json():
    new_dict = {
        "amenities": storage.count(amenity),
        "cities": storage.count(city),
        "places": storage.count(place),
        "reviews": storage.count(review),
        "states": storage.count(state),
        "users": storage.count(user),
    }
    return jsonify(new_dict)

