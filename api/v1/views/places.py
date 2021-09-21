#!/usr/bin/python3
"""
User for API.
"""
from api.v1.views.users import get_users
from models.city import City
from flask import abort, request, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Returns all places in jason format"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    list_place = []
    for place in city.places:
        if place.city_id == city_id:
            list_place.append(place.to_dict())
    return jsonify(list_place)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_id_place(place_id):
    """Returns city_id in json format"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place"""
    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates places"""
    places = request.get_json()

    if not places:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in places:
        return (jsonify({'error': 'Missing user_id'}), 400)
    if 'name' not in places:
        return (jsonify({'error': 'Missing name'}), 400)

    get_city = storage.get(City, city_id)
    if get_city is None:
        abort(404)

    get_user = storage.get("User", places['user_id'])
    if get_user is None:
        abort(404)

    places['city_id'] = city_id
    new_place = Place(**places)
    storage.new(new_place)
    storage.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Updates a place """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
