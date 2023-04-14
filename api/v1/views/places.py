#!/usr/bin/python3
"""
Create a new view that handles all default RESTFul API actions
get_all_place [GET]
get_place [GET]
delete_place [DELETE]
post_place [POST]
update_place [PUT]
"""
from models.place import Place
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def get_all_place():
    """returns HOW MANY DATA IN STORAGE"""
    places = storage.all(Place).values()
    return jsonify([place.to_dict() for place in places])


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    """retrieves a State object using id"""
    # retrieve all objects registered in the State class
    states = storage.all(Place)
    for key, value in states.items():
        # check if the state_id is linked to any State object
        if states[key].id == place_id:
            return value.to_dict()
    # if the state_id is not linkes to any State object raise an error
    abort(404)

@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_soms_cities(city_id):
    """retrieve the list of all City objects"""
    # retrieve states and IDs registered in the State class
    cities = storage.get(City, city_id)
    # raise an error if the state_id is not linked to any State object
    if cities is None:
        abort(404)
    else:
        cities = storage.all(City).values()
        list_places = [place.to_dict() for place in cities.places]
        return jsonify(list_places)

@app_views.route('places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """delete a State object"""

    place = storage.get(Place, place_id)

    # check if the id is linked to any State object, if not raise an error
    if place is None:
        abort(404)

    # delete a State object if the state_id is linked
    storage.delete(place)
    storage.save()

    # return an empty dictionary with the status code 200
    return (jsonify({}), 200)


@app_views.route('places', methods=['POST'], strict_slashes=False)
def post_place():
    """create a State object"""
    items = request.get_json()

    if items is None:
        abort(400, 'Not a JSON')

    if 'name' not in items:
        abort(400, 'Missing name')

    new_state = Place(**items)
    new_state.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a State object"""

    place = storage.get(Place, place_id)

    # raise an error if the state_id is not linked to any State object
    if place is None:
        abort(404)

    data = request.get_json()
    # raise an error if the HTTP body request is not valid JSON
    if data is None:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'created_at', 'updated_at']

    # update the State object with all key-value pairs of the dictionary
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()

    # return the State object with the status code 200
    return (jsonify(place.to_dict()), 200)
