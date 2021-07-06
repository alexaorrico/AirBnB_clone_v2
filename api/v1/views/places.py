#!/usr/bin/python3
""" View for place objects that handles all default RestFul API actions """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects of a City:
        GET /api/v1/cities/<city_id>/places
    """

    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    places = []
    for place in city.places:
        places.append(place.to_dict())

    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object. :
        GET /api/v1/places/<place_id>
    """

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object:
        DELETE /api/v1/places/<place_id>
    """

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return (jsonify({})), 200


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """ Creates a Place:
        POST /api/v1/cities/<city_id>/places
    """

    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    req_json = request.get_json()
    if not req_json:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' not in req_json:
        return jsonify({'error': 'Missing name'}), 400

    if 'user_id' not in req_json:
        return jsonify({'error': 'Missing user_id'}), 400

    else:
        user_id = req_json['user_id']
        user = storage.get(User, user_id)

        if user is None:
            abort(404)

    obj = Place(**req_json)
    setattr(obj, "city_id", city_id)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """ Updates a Place object:
        PUT /api/v1/places/<place_id>
    """

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    for attr, val in request.get_json().items():
        setattr(place, attr, val)

    place.save()
    return jsonify(place.to_dict()), 200
