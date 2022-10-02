#!/usr/bin/python3
"""view cities object"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def places_by_city(city_id):
    """return list of all object places"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    places = list()
    list_places = storage.all('Place')
    for value in list_places.values():
        if city_id == value.city_id:
            places.append(value.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def place_by_id(place_id):
    """Get places by ID"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_places(place_id):
    """Deletes an specific place"""
    ret = storage.get('Place', place_id)
    if ret:
        storage.delete(ret)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_places(city_id):
    """Create a new place"""
    from models.place import Place
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    content = request.get_json(force=True, silent=True)
    if not content:
        abort(400, "Not a JSON")
    if "user_id" not in content.keys():
        abort(400, "Missing user_id")
    if "name" not in content.keys():
        abort(400, "Missing name")

    user = storage.get('User', content["user_id"])
    if not user:
        abort(404)
    name_place = content.get('name')
    id = content.get('user_id')

    new_instance = Place(name=name_place, user_id=id)
    return jsonify(new_instance.to_dict()), 201


@app_views.route('/places/<places_id>', strict_slashes=False, methods=['PUT'])
def update_place(places_id):
    """Update a state by a given ID"""
    new_place = storage.get('Place', places_id)
    if not new_place:
        abort(404)

    content = request.get_json(force=True, silent=True)
    if not content:
        abort(400, "Not a JSON")

    to_ignore = ['id', 'user_id', 'city_id', 'created_at', 'update_at']
    for key, value in content.items():
        if key in to_ignore:
            continue
        else:
            setattr(new_place, key, value)
    storage.save()
    return jsonify(new_place.to_dict()), 200
