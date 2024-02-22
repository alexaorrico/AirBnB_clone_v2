#!/usr/bin/python3
"""
Create a new view for Place objects
that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.city import City
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models import storage
from models.user import User
from flasgger.utils import swag_from


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/get.yml', methods=['GET'])
def get_place_objects(city_id):
    """ Retrieves the list of all place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place/get_id.yml', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    dict_place = place.to_dict()
    return jsonify(dict_place)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/place/delete.yml', methods=['DELETE'])
def del_place(place_id):
    """ delete place by place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/user/post.yml', methods=['POST'])
def create_place(city_id):
    """creates a Place instance"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    info = request.get_json()
    user = storage.get(User, info['user_id'])
    if not user:
        abort(404)

    info['city_id'] = city_id
    place = Place(**info)
    return (jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/place/put.yml', methods=['PUT'])
def update_place(place_id):
    """updates Place object based on the id"""
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        attr_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in attr_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)
