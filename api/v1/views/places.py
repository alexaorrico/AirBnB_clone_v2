#!/usr/bin/python3
"""index default view"""

from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def all_places(city_id):
    """retrieves all Place objects by class name"""
    if not storage.get('City', city_id):
        abort(404)

    places = []
    for place in storage.all('Place').values():
        if place.city_id == city_id:
            places.append(place.to_dict())
    return jsonify(places)


@app_views.route("/places/<place_id>", strict_slashes=False)
def place(place_id):
    """retrieves the number of each objects by place_id"""
    place = storage.get("Place", place_id)
    if not plce:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """retrieves the number of each objects by place_id"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    '''Creates the required test case'''
    if not request.get_json():
        abort(400, description="Not a JSON")

    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    user_id = request.get_json().get('user_id')

    if not user_id:
        abort(400, description="Missing user_id")

    if not storage.get("User", user_id):
        abort(404)

    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    place = Place()
    place.name = request.get_json()['name']
    place.city_id = city_id
    place.user_id = user_id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'])
def update_place(place_id):
    '''Updates the target place with the corressponding id'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for k, v in request.get_json().items():
        if k == "id" or k == "created_at" or k == "updated_at"\
            or k == "user_id" or k == "city_id":
            continue
        else:
            setattr(place, k, v)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
