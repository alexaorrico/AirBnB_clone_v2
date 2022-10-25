#!/usr/bin/python3
""" Flask views for the Places resource """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_places(city_id):
    """ An endpoint that returns all places of a places """
    rlist = []
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    else:
        places = city.places
        for place in places:
            rlist.append(place.to_dict())
        return(jsonify(rlist))


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    """ An endpoint that returns a specific place """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """ An endpoint that deletes a specific place """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """ An endpoint that creates a specific place """
    req_fields = ['name', 'user_id']
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    for field in req_fields:
        if field not in content:
            abort(400, 'Missing {}'.format(field))
    user = storage.get('User', content['user_id'])
    if user is None:
        abort(404)
    content['city_id'] = city_id
    place = Place(**content)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def modify_place(place_id):
    """ An endpoint that modifies an existing place """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    ignore = ['id', 'created_at', 'updated_at', 'city_id', 'user_id']
    for k, v in content.items():
        if k not in ignore:
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200
