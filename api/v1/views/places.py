#!/usr/bin/python3
"""
file for "/api/v1/amenities" API
with GET, POST, PUT and DELETE
for getting, posting, putting and deleting
Place objects in 'storage', imported from
'models', and saving those changes in the
'storage's database/JSON file.
"""
from models.city import City
from models.user import User
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route(
        "/cities/<city_id>/places",
        strict_slashes=False
    )
def all_places_of_city_in_JSON(city_id):
    """
    Returns all Place objects in 'storage'
    related to the 'City' instance in 'storage'
    with 'city_id' as its 'id'.

    If the city doesn't exist,
    this function calls 'abort(404)'.
    """
    city = storage.get(City, city_id)

    if city is None:  # city doesn't exist
        abort(404)

    return jsonify(
        [
            place.to_dict()
            for place in city.places
        ]
    )


@app_views.route(
        "/places/<place_id>",
        strict_slashes=False,
        methods=["GET"]
    )
def get_place_by_id_in_JSON(place_id):
    """
    Returns the place with the 'place_id'
    argument and route in 'storage',
    in its JSON-serializable dict form,
    if the 'Place' object exists.

    Raises 404 otherwise.
    """
    result = storage.get(Place, place_id)

    if result is None:
        abort(404)

    return jsonify(result.to_dict())


@app_views.route(
        "/places/<place_id>",
        strict_slashes=False,
        methods=["DELETE"]
    )
def delete_place_by_id(place_id):
    """
    Deletes 'Place' object with 'place_id' as its 'id'
    field/column value (let's call it 'target')
    from 'storage.all' dictionary, by calling storage.delete(<target>).

    Returns ({}, 200) if successful,
    404 if 'target' doesn't exist.
    """
    target = storage.get(Place, place_id)

    if target is None:
        abort(404)
    storage.delete(target)
    storage.save()

    return jsonify({}), 200


@app_views.route(
        "/cities/<city_id>/places",
        strict_slashes=False,
        methods=["POST"]
    )
def post_place_in_JSON(city_id):
    """
    Creates new 'Place' object and relates it
    to the 'City' instance with 'city_id' as its
    'id' in 'storage'.

    If that city doesn't exist,
    this function calls 'flask.abort(404)'.
    (BEFORE checking if the request's
    JSON is valid)

    If the input provided isn't valid JSON,
    this function calls 'flask.abort(400, "Not a JSON")'.

    If the JSON provided in the request
    has no 'name' key,
    this function calls 'flask.abort(400, "Missing name")'.

    If the JSON provided in the request
    has no 'user_id' key,
    this function calls 'flask.abort(400, "Missing user_id").

    If any of the keys are not the way
    the 'Place' definition says, an error
    may occur. (Definition is in
    <project root>/models/place.py)

    Returns the new Place object as a JSON dictionary,
    and a status code of 200.
    """
    place_city = storage.get(City, city_id)

    if place_city is None:
        abort(404)

    new_place_in_JSON = request.get_json(silent=True)
    # If the request's JSON isn't valid,
    # 'new_place_in_JSON' is None.
    if new_place_in_JSON is None:
        abort(400, "Not a JSON")

    if 'name' not in new_place_in_JSON:
        abort(400, "Missing name")
    if 'user_id' not in new_place_in_JSON:
        abort(400, "Missing user_id")

    place_user = storage.get(User, new_place_in_JSON['user_id'])
    if place_user is None:
        abort(404)

    new_place_in_JSON['city_id'] = city_id

    new_place = Place(**new_place_in_JSON)
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route(
    "/places/<place_id>",
        strict_slashes=False,
    methods=["PUT"])
def put_place_in_JSON(place_id):
    """
    Overrides 'Place' object's attributes
    except 'id', 'created_at', 'updated_at'
    and '__class__',
    where the object's id is 'place_id',
    with the json attributes provided in the
    PUT request.

    If any of the keys are not the way
    the 'Place' definition says, an error
    may occur. (Definition is in
    <project root>/models/place.py)

    If the place with 'place_id' as its 'id'
    doesn't exist, this function calls
    abort(404).

    Otherwise, this function returns the JSON
    format of the new place with code 200.
    """
    place = storage.get(Place, place_id)

    if storage.get(Place, place_id) is None:
        abort(404)

    new_place_info = request.get_json(silent=True)
    # invalid JSON
    if new_place_info is None:
        abort(400, "Not a JSON")

    # We're changing 'place's attributes in-place.
    for attr, value in new_place_info.items():
        if attr not in ('id', 'created_at', 'updated_at', '__class__'):
            # skip those attributes
            place.__setattr__(attr, value)

    storage.save()
    # We have to re-write the object change
    # to the database/storage file,
    # so that the changes are saved
    # there too, and not just in this
    # Python object.

    return jsonify(place.to_dict()), 200
