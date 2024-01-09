#!/usr/bin/python3
"""Creates a new view for State objects that
handles all default RESTFul API actions"""
from flask import abort, jsonify, request
from models.state import State
from models.city import City
from models.amenity imprt Amenity
from api.v1.views import app_views
from models import storage


# route to get all amenity objects based on states
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """returns all amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


# route for getting an amenity obj based on its id
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """returns amenity obj for the id input"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


# route for deleting a file
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an amenity obj"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


# route for creating a file
@app_views.route('/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """creates an amenity obj"""
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


# route for updating a file
@app_views.route('amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def updateamenity(amenity_id):
    """updates a city obj"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if not request.get_json():
            abort(400, 'Not a JSON')

        """get JSON data from request"""
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        """update city obj with json data"""
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)
