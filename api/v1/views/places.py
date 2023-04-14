#!/usr/bin/python3
"""
create a new view that handles all default RESTFul API actions
"""
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """retrieve the list of all City objects"""
    # retrieve states and IDs registered in the State class
    city = storage.get(City, city_id)
    # raise an error if the state_id is not linked to any State object
    if city is None:
        abort(404)
    else:
        list_places = [place.to_dict() for place in city.places]
        return jsonify(list_places)


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """retrieve a City object"""
    # retrieve City objects and their IDs registered in the City class
    place = storage.get(Place, place_id)

    # raise an error if the city_id is not linked to any City object
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """delete a City object"""
    # retrieve all City objects registered in the City class
    place = storage.get(Place, place_id)

    # raise an error if the city_id doesn't match
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    # return an empty dictionary with the status code 200
    return (jsonify({}), 200)


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create a city object"""
    # get State object which is linked to the state_id
    city = storage.get(City, city_id)
    # raise an error if the state_id is not linked to any State object
    if city is None:
        abort(404)

    # transform the HTTP body request to a dictionary
    body = request.get_json()
    # raise error if the the HTTP body request is not a valid JSON
    if body is None:
        abort(400, 'Not a JSON')

    # raise error if the dictionary doesn’t contain the key name
    if 'name' not in body:
        abort(400, 'Missing name')

    if 'user_id' not in body:
        abort(400, 'Missing user_id')

    user = storage.get(User, body['user_id'])
    if user is None:
        abort(404)

    body['city_id'] = city_id
    place = Place(**body)
    storage.new(place)
    place.save()
    return (jsonify(place.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a City object"""
    # get a City object and its ID
    place = storage.get(Place, place_id)
    # raise error id city_id is not linked to any City object
    if place is None:
        abort(404)

    # transform the HTTP body request to a dictionary
    body = request.get_json()
    # raise error if the the HTTP body request is not a valid JSON
    if body is None:
        abort(400, 'Not a JSON')

    print(body['user_id'])
    if body['user_id'] is None:
        abort(400, 'Missing user_id')

    user = storage.get(User, body['user_id'])
    print(user)
    if user is None:
        abort(404)

    ignore_key = ['id', 'state_at', 'created_at' 'updated_at']
    for key, value in body.items():
        if key not in ignore_key:
            setattr(place, key, value)

    storage.save()
    return (jsonify(place.to_dict()), 200)
