#!/usr/bin/python
""" Module for state object view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/places', methods=['GET'],
                 strict_slashes=False)
def get_places():
    """ Returns all place objects """
    places_dict_list = [place.to_dict() for
                        place in storage.all("Place").values()]
    return jsonify(places_dict_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_id(state_id):
    """ Method retrieves place object with certain id """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Method deletes place object based off of its id """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/places', methods=['POST'],
                 strict_slashes=False)
def post_place():
    """ Method creates new place object """
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if body.get("name") == None:
        abort(400, "Missing name")
    place = Places(**body)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """ Method updates a place object based off its id """
    place = storage.get("Place", state_id)
    body = request.get_json()
    if not place:
        abort(404)
    if not body:
        abort(400, "Not a JSON")
    for k, v in body.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict())
