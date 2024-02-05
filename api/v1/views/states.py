#!/usr/bin/python3
"""
Defines the places view for the API, handling all default RESTful API actions.
"""
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def handle_places(city_id=None, place_id=None):
    """
    Handles all default RESTful API actions for Place objects.
    """
    handlers = {
        'GET': get_places,
        'POST': add_place,
        'DELETE': remove_place,
        'PUT': update_place
    }
    request_method = request.method
    if request_method in handlers:
        return handlers[request_method](city_id=city_id, place_id=place_id)
    abort(405)


def get_places(city_id=None, place_id=None):
    """
    Retrieves Place objects based on city_id or a specific place_id.
    """
    if city_id:
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    if place_id:
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        return jsonify(place.to_dict())
    abort(404)


def add_place(city_id=None, place_id=None):
    """
    Creates a new Place object within a specified City.
    """
    if not city_id or place_id:
        abort(404)
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, description="Not a JSON")
    if 'user_id' not in request_data:
        abort(400, description="Missing user_id")
    if 'name' not in request_data:
        abort(400, description="Missing name")
    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)
    new_place = Place(city_id=city_id, **request_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


def remove_place(city_id=None, place_id=None):
    """
    Deletes a specific Place object by place_id.
    """
    if not place_id:
        abort(404)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


def update_place(city_id=None, place_id=None):
    """
    Updates a specific Place object by place_id.
    """
    if not place_id:
        abort(404)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in request_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
