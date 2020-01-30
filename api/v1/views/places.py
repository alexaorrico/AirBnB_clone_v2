#!/usr/bin/python3
""" creates new view for place objects """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def list_all_places(city_id):
    """Reviews list of all Places in a City"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    all_places = storage.all('Place').values()
    city_places = [p.to_dict() for p in all_places if p.city_id == city_id]
    return jsonify(city_places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def list_place(place_id):
    """Retrieves place object """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a place object """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Adds another object to the storage"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    new_place_dict = request.get_json(silent=True)
    if new_place_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    elif 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    user_id = new_place_dict['user_id']
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    new_place_dict['city_id'] = city_id
    new_place = Place(**new_place_dict)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places_search', methods=['POST'])
def search_places():
    """ search places depending on state and city and amenity id"""
    form = request.get_json(force=True)
    place_list = []
    all_cities = []
    all_amenities = []
    all_places = []
    if len(form) == 0:
        all_places = storage.all('Place')
        for place in all_places.values():
            place_list.append(place.to_dict())
        return jsonify(place_list), 200
    if 'cities' in request.json:
        for city_id in form['cities']:
            all_cities.append(storage.get('City', 'city_id'))
    if 'states' in request.json:
        for state_id in form['states']:
            for city in storage.get('State', state_id).cities:
                if city not in all_cities:
                    all_cities.append(city)
    for city in all_cities:
        for place in city.places:
            all_places.append(place)

    if 'amenities' in request.json and len(all_places) != 0:
        for amenity_id in form['amenities']:
            all_amenities.append(storage.get('Amenity', amenity_id))
        for amenity in all_amenities:
            for place in all_places:
                if place not in amenity.place_amenities:
                    all_places.remove(place)
    if 'amenities' in request.json and len(all_places) == 0:
        for amenity_id in form['amenities']:
            all_amenities.append(storage.get('Amenity', amenity_id))
        for amenity in all_amenities:
            for place in amenity.place_amenities:
                place_list.append(place.to_dict())
        return jsonify(place_list), 200

    for place in all_places:
        place_list.append(place.to_dict())
    return jsonify(place_list), 200


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates an instance of Place"""
    update_place_json = request.get_json(silent=True)
    if update_place_json is None:
        return jsonify({'error': 'Not a JSON'}), 400
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    ignore = ['id', 'created_at', 'updated_at', 'city_id', 'user_id']
    for k, v in update_place_json.items():
        if k not in ignore:
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200
