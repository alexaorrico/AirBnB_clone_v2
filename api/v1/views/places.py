#!/usr/bin/python3
""" handles all default RESTFul API actions for Place """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places(city_id):
    """
        retrieves list of all Places of a specific city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        places_list = []
        for place in city.places:
            places_list.append(place.to_dict())
    return (jsonify(places_list))


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def place_by_id(place_id):
    """
        retrieves specific Places
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        place_dict = place.to_dict()
        return (jsonify(place_dict))


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
        delete specific place with given id
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
        create Place
    """
    # get the linked city
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    #  transform the HTTP body request to a dictionary
    json_data = request.get_json()

    if not json_data:
        return (jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in json_data:
        return (jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in json_data:
        return (jsonify({"error": "Missing name"}), 400)
    json_data['city_id'] = city_id
    # get linked user if exist
    user = storage.get(User, json_data['user_id'])
    if user is None:
        abort(404)
    # State(**kwargs)
    newplace = Place(**json_data)
    newplace.save()
    # transform object in valid json
    newplace_dict = newplace.to_dict()
    return (jsonify(newplace_dict), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
        update State
    """
    #  transform the HTTP body request to a dictionary
    json_data = request.get_json()
    if not json_data:
        return (jsonify({"error": "Not a JSON"}), 400)

    # get given state
    given_place = storage.get(Place, place_id)
    # if no Place with right id
    if given_place is None:
        abort(404)

    # replace
    for key, value in json_data.items():
        # update item except this 3
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(given_place, key, value)

    storage.save()
    # transform object in valid json
    newplace_dict = given_place.to_dict()
    return (jsonify(newplace_dict), 200)
