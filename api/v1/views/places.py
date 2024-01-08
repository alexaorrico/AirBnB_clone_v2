#!/usr/bin/python3
"""place view"""
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all cities objects"""
    from models import storage
    from models.city import City
    places_list = []
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """Retrieves a place object"""
    from models import storage
    from models.place import Place
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a place object"""
    from models import storage
    from models.place import Place
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Creates a place"""
    from models import storage
    from models.place import Place
    from models.city import City
    from models.user import User
    from flask import request

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        return abort(404)
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400

    city = storage.get(City, city_id)
    if city is None:
        return abort(404)

    place = Place(**request.get_json())
    place.city_id = city_id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates a place object"""
    from models import storage
    from models.place import Place
    from flask import request
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id' 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
