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
    """Return places according for city id or return error message
    """
    if city_id:
        dict_c = storage.get(City, city_id)
        if dict_c is None:
            abort(404)
        else:
            places = storage.all(Place).values()
            list_pl = []
            for place in places:
                if place.city_id == city_id:
                    list_pl.append(place.to_dict())
            return jsonify(list_pl)


@app_views.route('places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """Return place for id or return error message
    """
    if place_id:
        dict_pl = storage.get(Place, place_id)
        if dict_pl is None:
            abort(404)
        else:
            return jsonify(dict_pl.to_dict())


@app_views.route('places/<place_id>', strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """Deletes one place if exists, or retunr error message
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
    """Create a new place or raise Error if is not a
        valid json or if the name is missing
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
    """Updates attributes for one place"""
    if place_id:
        obj_places = storage.get(Place, place_id)
        if obj_places is None:
            abort(404)

        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        attr = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for k, v in req.items():
            if k not in attr:
                setattr(obj_places, k, v)
        obj_places.save()
        return make_response(jsonify(obj_places.to_dict()), 200)
