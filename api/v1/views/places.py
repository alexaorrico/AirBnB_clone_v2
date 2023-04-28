#!/usr/bin/python3
"""View of Places for RESTFul API"""

from api.v1.views import app_views, validate_model, get_json
from flask import jsonify
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = validate_model("City", city_id)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = validate_model("Place", place_id)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = validate_model("Place", place_id)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def place_no_id_post(city_id):
    """Creates a Place"""
    city = validate_model("City", city_id)
    req_json = get_json(['user_id', 'name'])
    user_id = req_json.get('user_id')
    user = validate_model("User", user_id)
    req_json['city_id'] = city_id
    new_object = Place(**req_json)
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def place_with_id_put(place_id):
    """Updates a Place object"""
    place_obj = validate_model("Place", place_id)
    req_json = get_json()
    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in req_json.items():
        if key not in ignore_keys:
            setattr(place_obj, key, value)
    place_obj.save()
    return jsonify(place_obj.to_dict())
