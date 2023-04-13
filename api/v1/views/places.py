#!/usr/bin/python3
"""First route to display a json object"""
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, request
from models import storage
from api.v1.views import app_views


@app_views.route('/places/', methods=['GET', 'POST'],
                 defaults={'place_id': None})
@app_views.route('/places/<place_id>',
                 methods=['GET', 'POST', 'DELETE', 'PUT'])
def places_views(place_id=None):
    if place_id is not None:
        new_place = storage.get(Place, place_id)
        if new_place is None:
            return jsonify(error='Place not found'), 404
        # Get method with id works
        if request.method == 'GET':
            return jsonify(new_place.to_dict())
        if request.method == 'DELETE':
            storage.delete(new_place)
            storage.save()
            return {}, 200
        if request.method == 'PUT':
            update_values = request.get_json()
            if type(update_values) is not dict:
                return jsonify(error='Not a JSON'), 400
            for key, val in update_values.items():
                ls = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
                if key not in ls:
                    setattr(new_place, key, val)
                storage.save()
            return jsonify(new_place.to_dict())
    else:
        # Get method works
        if request.method == 'GET':
            new_places = storage.all(Place)
            json_places = []
            for place in new_places.values():
                json_places.append(place.to_dict())
            return jsonify(json_places)


@app_views.route('/cities/<city_id>/places/', methods=['GET', 'POST'])
def place_by_city(city_id):
    """ city view model"""
    city = storage.get(City, city_id)
    places = storage.all(Place)
    if city is None:
        return jsonify(error='No city found'), 404
    # Get method works with city_id
    if request.method == "GET":
        place_list = []
        for place in places.values():
            if place.city_id == city_id:
                place_list.append(place.to_dict())
        return jsonify(place_list), 200
    elif request.method == 'POST':
        update_values = request.get_json()
        if type(update_values) is not dict:
            return jsonify(error='Not a JSON'), 400
        if 'user_id' not in update_values.keys():
            return jsonify(error='Missing user_id'), 400
        if 'name' not in update_values.keys():
            return jsonify(error='Missing name'), 400
        user = storage.get(User, update_values['user_id'])
        if user is None:
            return jsonify(error='Missing user_id'), 404
        x = Place(
            name=update_values['name'], city_id=city_id,
            user_id=update_values['user_id'])
        return jsonify(x.to_dict()), 201
