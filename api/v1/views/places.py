#!/bin/bash python3
""" place view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, render_template, abort
from models import storage
from models.place import Place
from models.base_model import BaseModel


@app_views.route('/places', methods=["GET"], strict_slashes=False)
def get_all_places():
    """ retrieves all place objects """
    output = []
    places = storage.all(Place).values()
    for place in places:
        output.append(place.to_dict())
    return (jsonify(output))


@app_views.route('/places/<place_id>', methods=["GET"], strict_slashes=False)
def get_a_place(place_id):
    """ retrieves one unique place object """
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
            output = place.to_dict()
            return (jsonify(output))
    return jsonify({"error": "Not found"}), 404


@app_views.route('/places/<place_id>', methods=["GET", "DELETE"], strict_slashes=False)
def del_a_place(place_id):
    """ delete one unique place object """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(place)
    storage.save()
    result = make_response(jsonify({}), 200)
    return result
