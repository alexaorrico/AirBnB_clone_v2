#!/usr/bin/python3
"""View for Places"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.place import Place
from models.city import City
from models.user import User
from flask import abort
from flask import make_response
from flask import request


@app_views.route('cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_places(city_id):
    """Return places according to id of city object
        or return error: Not found if it doesn't exist.
    """
    if city_id:
        dict_city = storage.get(City, city_id)
        if dict_city is None:
            abort(404)
        else:
            places = storage.all(Place).values()
            list_places = []
            for place in places:
                if place.city_id == city_id:
                    list_places.append(place.to_dict())
            return jsonify(list_places)


@app_views.route('places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """Return place according class and id of the place
        or return Error: Not found if it doesn't exist.
    """
    if place_id:
        dict_place = storage.get(Place, place_id)
        if dict_place is None:
            abort(404)
        else:
            return jsonify(dict_place.to_dict())


@app_views.route('places/<place_id>', strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """Deletes an object Place if exists, otherwise raise
        404 error
    """
    if place_id:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        else:
            storage.delete(place)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def response_place(city_id):
    """Post request that allow to create a new place if exists the name
        or raise Error if is not a valid json or if the name is missing
    """
    if city_id:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()

    if "user_id" not in req:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    user = storage.get(User, req['user_id'])
    if user is None:
        abort(404)

    if "name" not in req:
        return make_response(jsonify({"error": "Missing name"}), 400)
    req['city_id'] = city_id
    places = Place(**req)
    places.save()
    return make_response(jsonify(places.to_dict()), 201)


@app_views.route('places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """Updates attributes from an place object"""
    if place_id:
        obj_places = storage.get(Place, place_id)
        if obj_places is None:
            abort(404)

        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        for key, value in req.items():
            if key not in [
                'id',
                'user_id',
                'city_id',
                'created_at',
                    'updated_at']:
                setattr(obj_places, key, value)
        obj_places.save()
        return make_response(jsonify(obj_places.to_dict()), 200)
