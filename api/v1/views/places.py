#!/usr/bin/python3
'''Contains the place view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route(
    '/api/v1/cities/<city_id>/places',
    methods=["GET"])
def get_places(city_id):
    """
    Retrieves the list of all City objects
    for a specified State
    """
    city = storage.get('City', city_id)
    if not city:
        abort(404)

    places = [palce.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route(
    '/api/v1/places/<place_id>',
    methods=["GET"]
    )
def get_place(place_id):
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route(
    '/api/v1/places/<place_id>',
    methods=["DELETE"])
def delete_place(place_id):
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return {}, 200


@app_views.route(
    "/api/v1/cities/<city_id>/places",
    methods=["POST"]
    )
def post_place(city_id):
    city = storage.get("City", city_id)
    if not city:
        abort(city)

    try:
        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if data.get('user_id') is None:
            return make_response(jsonify({'error': 'Missing user_id'}))
        else:
            user_id = data.get('user_id')
            user = storage.get("User", user_id)
            if not user:
                abort(404)
        if data.get('name') is None:
            return make_response(jsonify({'error': 'Missing name'}), 400)
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data.update({"city_id": city_id})
    obj = Place(**data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route(
    '/places/<place_id>',
    methods=['PUT'],
    strict_slashes=False)
def update_city(place_id):
    """update operation"""
    obj = storage.get("Place", place_id)
    if not obj:
        abort(404)

    try:
        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if data.get('name') is None:
            return make_response(jsonify({'error': 'Missing name'}), 400)
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for k, v in data.items():
        if k not in ['user_id', 'id', 'created_at', 'updated_at']:
            setattr(obj, k, v)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
