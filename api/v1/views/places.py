#!/usr/bin/python3
"""Place API"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<string:city_id>/places", strict_slashes=False,
                 methods=['GET'])
def get_city_places(city_id):
    """Returns all places objects in a city"""

    city = storage.get(City, city_id)
    if city is not None:
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    else:
        return jsonify({'error': 'Not found'}), 404


@app_views.route("/places/<string:place_id>", strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    """Returns a place with a given id"""

    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify(place.to_dict())
    else:
        return jsonify({'error': 'Not found'}), 404


@app_views.route("/places/<string:place_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """Delete a place"""
    place = storage.get(Place, place_id)
    if place is not None:
        place.delete()
        return jsonify({})
    return jsonify({'error': 'Not found'}), 404


@app_views.route("/cities/<string:city_id>/places", strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """Create a place"""

    city = storage.get(City, city_id)
    if city is not None:
        if request.is_json:
            data = request.get_json()
            user_id = data.get('user_id', None)
            place_name = data.get('name', None)
            if user_id is None:
                return jsonify({'error': 'Missing user_id'}), 400
            user = storage.get(User, user_id)
            if user is None:
                return jsonify({'error': 'Not found'})
            if place_name is None:
                return jsonify({'error': 'Missing name'}), 400
            place = Place(user_id=user_id,
                          city_id=city_id,
                          name=place_name)
            place.save()
            return jsonify(place.to_dict()), 201
        return jsonify({'error': 'Not a JSON'}), 400
    return jsonify({'error': 'Not found'}), 404


@app_views.route("/places/<string:place_id>", strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    """Updates a place"""
    place = storage.get(Place, place_id)
    if place is not None:
        if request.is_json:
            data = request.get_json()
            data = {k: v for k, v in data.items() if k != 'id' and
                    k != 'created_at' and k != 'updated_at' and
                    k != 'user_id' and k != 'city_id'}
            for k, v in data.items():
                setattr(place, k, v)
            place.save()
            return jsonify(place.to_dict()), 200
        return jsonify({'error': 'Not a JSON'}), 400
    return jsonify({'error': 'Not found'}), 404
