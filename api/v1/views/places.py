#!/usr/bin/python3
'''Contains the places view for the API.'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a new place object """
    # grab the city object from storage
    city = storage.get(City, city_id)

    if city is None:  # if city_id isnt found in storage
        abort(404)

    # if body doesn't contain valid JSON
    if not request.is_json:
        abort(400, "Not a JSON")

    # else transform HTTP body into a dict
    body = request.get_json()

    # if the user_id key doesnt exist in the body dict
    user_id = body.get("user_id")
    if user_id is None:
        abort(400, "Missing user_id")

    # check using user_id to see if user exists in storage
    if storage.get(User, user_id) is None:  # user_id not found in storage
        abort(404)

    # if the text key doesnt exist in the body dict
    if body.get("name") is None:
        abort(400, "Missing name")

    # create and save the new place instance
    body['city_id'] = city_id
    new_place = Place(**body)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def retrieve_places(city_id):
    """ Retrieves a list of all Place objects of a City """
    # grab the city object from storage
    city = storage.get(City, city_id)

    if city is None:  # if city_id isnt found in storage
        abort(404)

    # convert all place objects into dictionaries & put in list
    place_list = [place.to_dict() for place in city.places]

    # return the list of places
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def retrieve_place(place_id):
    """ Retrieves a single place object based on its place_id """
    # grab the place object from storage
    place = storage.get(Place, place_id)

    if place:  # return the jsonified object
        return jsonify(place.to_dict())
    else:  # else if place is None
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates specific instance of a place object """
    # retrieve the object by place_id if it exists
    place = storage.get(Place, place_id)

    # abort if place with specific place_id can't be found
    if place is None:
        abort(404)

    # if body doesn't contain valid JSON
    if not request.is_json:
        abort(400, "Not a JSON")

    # else transform HTTP body into a dict
    body = request.get_json()

    # ignore id, created_at, updated_at keys during update
    excluded_keys = ["id", "user_id", "city_id" "created_at", "updated_at"]

    # iterate over body dict & update the place object
    # with the new values from body dict
    for key, value in body.items():
        if key not in excluded_keys:
            setattr(place, key, value)

    # save the updated place instance
    place.save()

    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes specific instance of a place object """
    # retrieve the object by place_id if it exists
    place = storage.get(Place, place_id)

    # delete the object if it exists
    if place:
        place.delete()
        storage.save()
        return jsonify({}), 200
    else:  # else if place is None
        abort(404)
