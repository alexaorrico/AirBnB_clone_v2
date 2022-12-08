#!/usr/bin/python3
"""
places
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['GET'])
def get_places(city_id):
    """ Get All places"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])
    


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    """ Get user with Id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """ DELETE user With id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['POST'])
def post_place(city_id):
    """ Crate place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
   
    try:
        body = request.get_json()

        if body is None:
            abort(400, description="Not a JSON")
        elif body.get('user_id') is None:
            abort(400, description='Missing user_id')  
        elif body.get('name') is None:
            abort(400, description='Missing name')
        else:
            user = storage.get(User, body.user_id)
            if user is None:
                abort(404)
            obj = Place(**body)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    except ValueError:
        abort(400, desciption="Not a JSON")


@app_views.route('/places/<user_id>', methods=["PUT"])
def update_place(place_id):
    """UPDATE a single places"""
    found = storage.get(Place, place_id)
    if not found:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        else:
            invalid = ['id', 'created_at', 'updated_at', 'email']
            for key, value in req.items():
                if key not in invalid:
                    setattr(found, key, value)
            storage.save()
            return jsonify(found.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")
