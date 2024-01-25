#!/usr/bin/python3
"""Creates a new view for Review objects that
handles all default RESTFul API actions"""
from flask import abort, jsonify, request
from flask_cors import CORS
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage


# route to get all review objects
@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """returns all review objects"""
    city = storage.all(City, city_id)
    if not city:
        abort(404)
    place_l = [place.to_dict() for place in city.places]
    return jsonify(place_l)


# route for getting a place obj based on its id
@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """returns place obj for the id input"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


# route for deleting a a place obj using its id
@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """deletes a place obj"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


# route for creating a place obj
@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates a place obj"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    """ transform the HTTP body request to a dictionary"""
    kwargs = request.get_json()
    if 'name' not in kwargs:
        abort(400, 'Missing name')
    if 'user_id' not in kwargs:
        abort(400, 'Missing user_id')

    user = storage.get(User, kwargs['user_id'])
    if not user:
        abort(404)

    kwargs['city_id'] = city_id
    place = Place(**kwargs)
    place.save()

    return jsonify(place.to_dict()), 201


# route for updating a user obj
@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """updates a place obj"""
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            abort(400, 'Not a JSON')

        """get JSON data from request"""
        new = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        """update place obj with json data"""
        for key, value in new.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)
