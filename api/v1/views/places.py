#!/usr/bin/python3
"""
view for Place  objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User

# users = []
# users_dict = storage.all(User)
# for k, v in users_dict.items():
#     users.append(v.to_dict())

# places = []
# places_dict = storage.all(Place)
# for k, v in places_dict.items():
#     places.append(v.to_dict())

# cities = []
# cities_dict = storage.all(City)
# for k, v in cities_dict.items():
#     cities.append(v.to_dict())


@app_views.route('/cities/<city_id>/places')
def get_cities_of_places(city_id):
    """Retrieves the list of all Place objects linked to a City"""
    city = storage.get(City, city_id)
    places = storage.all(Place)
    if not city:
        abort(404)
    city_places = [
        place.to_dict()
        for place in places.values() if place.city_id == city_id
        ]
    return jsonify(city_places)


@app_views.route('/places/<place_id>')
def get_place(place_id):
    """"Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    all_cities = storage.all(Place)
    if not place:
        abort(404)
    for k, v in all_cities.items():
        if v.id == place_id:
            v.delete()
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def add_place(city_id):
    """creates a Place (linked to a City by id)"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
    if 'name' not in request.get_json():
        return ("Missing name\n", 400)
    if 'user_id' not in request.get_json():
        return ("Missing user_id\n", 400)
    else:
        if 'user_id' in request.get_json():
            user = storage.get(User, request.get_json()['user_id'])
            if not user:
                abort(404)
    request_data = request.get_json()
    request_data['user_id'] = user.id
    request_data['city_id'] = city_id
    new_place = Place(**request_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """updates a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
    request_data = request.get_json()
    request_data.pop('id', None)
    request_data.pop('user_id', None)
    request_data.pop('city_id', None)
    request_data.pop('created_at', None)
    request_data.pop('updated_at', None)
    for key in request_data:
        setattr(place, key, request_data[key])
    place.save()
    return jsonify(place.to_dict()), 200
