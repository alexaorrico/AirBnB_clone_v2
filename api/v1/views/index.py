#!/usr/bin/python3
''' Status of your API '''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route('/stats')
def count():
    response = {
                "amenities": storage.count(State),
                "cities": storage.count(City),
                "places": storage.count(Place),
                "reviews": storage.count(Review),
                "states": storage.count(State),
                "users": storage.count(User),
            }
    return jsonify(response)
