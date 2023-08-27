from flask import request, jsonify, abort
from api.v1.views import app_views
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    amenities = Amenity.get_all()
    return jsonify([amenity.to_dict() for amenity in amenities]), 200

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    amenity = Amenity.get(amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict()), 200

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    amenity = Amenity.get(amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    amenity = Amenity.get(amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
