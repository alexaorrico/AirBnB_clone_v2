#!/usr/bin/python3
"""
module that defines API interactions for Places __objects
"""
from models import storage
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_places(city_id):
    """
    defines the places route
    Returns: list of all Place objects associated with a City obj
    """
    city = storage.get("City", city_id)
    if city:
        return jsonify([place.to_dict() for place in city.places])
    abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['GET'])
def id_for_place(place_id):
    """
    defines the places/<place_id> route
    Returns: place id or 404 Error if object not linked to Place object
    """
    a_place = storage.get("Place", place_id)
    if a_place:
        return jsonify(a_place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place_id(place_id):
    """
    defines Delete for Place objects by id
    Returns: if successful 200 and an empty dictionary
             404 if place_id is not linked to any Place obj
    """
    place = storage.get("Place", place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """
    define how to create a new place object
    Returns: 201 on successful creation
             400 "Not a JSON" if HTTP body request is not valid
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    body = request.get_json()
    if not body:
        return make_response('Not a JSON', 400)
    if not body.get("user_id"):
        return make_response('Missing user_id', 400)
    user = storage.get("User", body.get("user_id"))
    if not user:
        abort(404)
    if not body.get("name"):
        return make_response('Missing name', 400)
    place = Place(
                  name=body.get("name"),
                  user_id=body.get("user_id"),
                  city_id=city_id
                  )
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['PUT'])
def place_update(place_id):
    """
    defines how an Update to a place is made
    Returns: 200 and the place object if successful
             400 "Not a JSON" if HTTP body request is not valid
             404 if state_id is not linked to any Place object
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    body = request.get_json()
    if not body:
        return make_response('Not a JSON', 400)
    for key, value in body.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()

    return make_response(jsonify(place.to_dict()), 200)
