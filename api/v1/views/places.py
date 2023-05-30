#!/usr/bin/python3
"""Places module """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/cities')
def all_places(city_id):
    """Returns a list of places"""
    if not storage.get("City", city_id):
        abort(404)

    all_places = []
    for place in storage.all("Places").values():
        if place.city_id == city_id:
            all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route('/places/<place_id>')
def get_method_place(place_id):
    """Returns an instance of a place object object"""
    place = storage.get("place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<places_id>', methods=['DELETE'])
def del_method_place(place_id):
    """deletes place"""
    place = storage.get("Place", place_id)

    if Place is None:
        abort(404)
    storage.delete()
    storage.save()
    return make_response(jsonify({}, 200))


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_place(city_id):
    """creates a place"""
    if not storage.get("City", city_id):
        abort(404)

    if not request.get_json():
         abort(400, description= "Not a JSON")
  
    user_id = request.get_json().get('user_id')
    if not user_id:
        abort(400, decription="Missing user_id")

    if not storage.get("User", user_id):
        abort(404)
    
    if not request.get_json().get('name'):
        abort(400, description='Missing name')

    place = Place()
    place.name = request.get_json().get('name')
    place.city_id = city_id
    place.user_id = user_id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """updates place module"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    place = storage.get("Place", Place_id)

    if place is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(place, key, value)

    storage.save()
    return make_response(jsonify(place.to_dict(), 200))
