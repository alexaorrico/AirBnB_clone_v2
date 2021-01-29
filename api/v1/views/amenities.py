#!/usr/bin/python3
""" a new view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>/', methods=['GET'], strict_slashes=False)
def amenities_get(amenity_id=None):
    """retrieves the list of all State objects
    """
    if amenity_id is None:
        amenity = storage.all("Amenities").values()
        json_amenities = jsonify([amenity.to_dict() for amenity in list])
        return json_amenities

    try:
        amenities_info = jsonify(storage.get('Amenities', amenity_id).to_dict())
        return amenities_info
    except:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id):
    """deletes a State object
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        return jsonify(abort(404))
    amenity.delete()
    storage.save()
    dict = {}
    return (jsonify(dict), 200)


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def post_amenity():
    """creates a state
    """
    info = request.get_json()
    if info is None:
        return jsonify(abort(400, 'Not a JSON'))

    name = info.get('name')
    if name is None:
        return jsonify(abort(400, 'Missing name'))

    amenity_post = State(**info)
    amenity_post.save()

    return (jsonify(amenity_post.to_dict()), 201)


@app_views.route('/amenity/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_states(amenity_id):
    """updates a state object
    """
    info = request.get_json()
    if info is None:
        return jsonify(abort(400, 'Not a JSON'))

    amenity_info = storage.get("Amenity", state_id)
    if amenity_info is None:
        abort(404)

    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in info.items():
        if key not in ignore_keys:
            setattr(amenity_info, key, value)

    amenity_info.save()
    return jsonify(amenity_info.to_dict())
