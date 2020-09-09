#!/usr/bin/python3
"""comment"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.place import Place
from models.city import City


@app_views.route('/api/v1/cities/<city_id>/places')
def get_places():
    """our hearts pump dust and our hairs all grey"""
    lizt = []
    places = storage.all(Place).values()
    for place in places:
        if place.city_id == city_id:
            lizt.append(place.to_dict())
    return jsonify(lizt)


@app_views.route('/api/v1/places/<place_id>')
def get_a_place():
    """comment"""
    lizt = []
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
            lizt = place.to_dict()
            return jsonify(lizt)
    return jsonify({"error": "Not found"}), 404


@app_views.route('/api/v1/places/<place_id>', methods=['DELETE'])
def del_a_place():
    """comment"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
