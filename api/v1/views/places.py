#!/usr/bin/python3
"""comment"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, Blueprint
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places')
def get_places(city_id):
    """our hearts pump dust and our hairs all grey"""
    lizt = []
    places = storage.all(Place).values()
    for place in places:
        if place.city_id == city_id:
            lizt.append(place.to_dict())
    return jsonify(lizt)


@app_views.route('/places/<place_id>')
def get_a_place(place_id):
    """comment"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    ret = places.to_dict()
    return jsonify(ret)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def del_a_place(place_id):
    """comment"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    storage.delete(places)
    storage.save()
    return jsonify({}), 200
