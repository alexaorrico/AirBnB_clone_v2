#!/usr/bin/python3
'''place view for API'''

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    '''list all place object of a given city'''
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404, 'Not found')
    if city_id:
        objs = storage.all('Place').values()
        obj_list = []
        for obj in objs:
            if (city_id == obj.city_id):
                obj_list.append(obj.to_dict())
        return jsonify(obj_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def single_place(place_id):
    '''Retrieve place object'''
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    '''delete place object'''
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    '''return new place'''
    new_obj = request.get_json()
    if not new_obj:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if not City:
        abort(404)
    if 'name' not in new_obj:
        abort(400, "Missing name")
    obj = City(**new_obj)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    '''update place object'''
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k not in ['id','user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
