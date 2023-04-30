#!/usr/bin/python3
"""

Flask web server creation to handle api petition-requests

"""
from flask import jsonify, abort
from flask import request
from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def all_places(city_id):
    """
    Retrieves the list of all Place objects
    """
    city = storage.get(classes["City"], city_id)
    if city is None:
        abort(404)
    my_list = []
    for place in city.places:
        my_list.append(place.to_dict())
    return jsonify(my_list)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def some_place(place_id):
    """
    Retrieves a Place object if id is linked to some Place object
    """
    some_objs = storage.get(classes["Place"], place_id)
    if some_objs is None:
        abort(404)
    some_objs = some_objs.to_dict()
    return jsonify(some_objs)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_place(place_id):
    """
    Deletes a Place object if id is linked to some Place object
    """
    some_objs = storage.get(classes["Place"], place_id)
    if some_objs is None:
        abort(404)
    storage.delete(some_objs)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def post_place(city_id):
    """
    Create a new Place object
    """
    city_obj = storage.get(classes["City"], city_id)
    if city_obj is None:
        abort(404)
    data_json = request.get_json(force=True, silent=True)
    if (type(data_json) is not dict):
        abort(400, "Not a JSON")
    if "user_id" not in data_json:
        abort(400, "Missing user_id")
    user_obj = storage.get(classes["User"], data_json["user_id"])
    if user_obj is None:
        abort(404)
    if "name" not in data_json:
        abort(400, "Missing name")
    else:
        new_place = classes["Place"](city_id=city_id, **data_json)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places_search', strict_slashes=False, methods=['POST'])
def post_place_search():
    data_json = request.get_json(force=True, silent=True)
    if (type(data_json) is not dict):
        abort(400, "Not a JSON")
    if data_json == {}:
        all_places = storage.all(classes["Place"])
        return all_places


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def put_place(place_id):
    """
    Update a Place object
    """
    obj = storage.get(classes["Place"], place_id)
    if obj is None:
        abort(404)
    data_json = request.get_json(force=True, silent=True)
    if (type(data_json) is not dict):
        abort(400, "Not a JSON")
    for key, value in data_json.items():
        if key in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            continue
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
