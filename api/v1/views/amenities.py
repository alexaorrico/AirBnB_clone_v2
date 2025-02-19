#!/usr/bin/python3
"""
Creates API endpoints for acessing, creating,  deleting and
updating Amenity resources, it uses the app_views blueprint
"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, request, abort


@app_views.route('/amenities', strict_slashes=False,
                 methods=['GET'])
def get_amenities():
    """
    Retrieves all amenity objects and returns the JSON
    representation of the dictionary
    """
    amenities = []
    all_amenities = storage.all(Amenity)

    for amenity in all_amenities.values():
        amenities.append(amenity.to_dict())
    return (jsonify(amenities))


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_an_amenity(amenity_id):
    """
    Retrieves a specific amenity based on it's id
    404 error if the amenity does not exist
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is not None:
        return (jsonify(amenity.to_dict()))
    abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Deletes an amenity based on it's id
    Returns an empty dictionary plus 200ok status on success
    or 404 error page on failure
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()

    return (jsonify({})), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """
    Creates an amenity and returns the dictionary representation of the
    amenity, or an error dictionary
    """
    data = request.get_json()
    if not isinstance(data, dict):
        return (jsonify({'error': 'Not a JSON'}))
    if 'name' not in data.keys():
        return (jsonify({'error': 'Missing name'}))

    name = data.get('name')
    amenity = Amenity(name=f'{data.get('name')}')
    storage.new(amenity)
    storage.save()
    return (jsonify(amenity.to_dict())), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """
    Updates an amenity based on the id, returns a code 201
    on success or an error dictionary
    """
    data = request.get_json()

    if not isinstance(data, dict):
        return (jsonify({'error': 'Not a JSON'}))

    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    exclude = ['id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in exclude:
            setattr(amenity, k, v,)

    amenity.save()
    return (jsonify(amenity.to_dict())), 200
