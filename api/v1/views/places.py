#!/usr/bin/python3
""" places view """
from flask import Flask, Blueprint
from flask import abort, make_response
from flask import jsonify, request
from models import storage, city, place
from api.v1.views import app_views


@app_views.route('/places',
                 methods=['GET'],
                 strict_slashes=False)
def retrieve_places():
    """ retrieve all places """
    places = []
    all_places = storage.all('Place').values()
    for place in all_places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_a_place(city_id):
    """ Retrieves the list of all Place objects of a City """
    places = []
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    for my_place in my_city.places:
        places.append(my_place.to_dict())
    return jsonify(places)
