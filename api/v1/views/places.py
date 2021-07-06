#!/usr/bin/python3
''' a new view for City objects that handles all default RestFul API '''
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_all_places_of_city(city_id=None):
    ''' retrieves a list of all place objects of a given city '''
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    places = storage.all('Place')
    city_list = []
    for val in places.values():
        if val.city_id == city_id:
            city_list.append(val.to_dict())

    return jsonify(city_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_places(place_id=None):
    ''' returns an individual place object given a place id '''
    obj = storage.get('Place', place_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    ''' deletes an individual city '''
    obj = storage.get('Place', place_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404)

    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"],
                 strict_slashes=False)
def create_place(city_id=None):
    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in args:
        return jsonify({"error": "Missing name"}), 400
    elif 'user_id' not in args:
        return jsonify({"error": "Missing user_id"}), 400

    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    user_id = args['user_id']
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    args['city_id'] = city_id
    obj = Place(**args)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_places(place_id=None):
    ''' updates an individual city '''
    obj = storage.get('Place', place_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404)

    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400

    for k, v in args.items():
        if k not in ["id", "city_id", "user_id", "updated_at", "created_at"]:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
