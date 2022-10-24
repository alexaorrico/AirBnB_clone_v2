#!/usrr/bin/python3
"""Flask app index page to display status"""
from flask import Flask, jsonify, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def getStatus():
    """Return JSON status: OK"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def getCount():
    """Returns count"""
    count_dict = {"amenities": 'Amenity', "cities": 'City',
                  "places": 'Place', "reviews": 'Review',
                  "states": 'State', "users": 'User'}

    for i in count_dict.keys():
        count_dict[i] = storage.count(count_dict.get(i))
    return jsonify(count_dict)
