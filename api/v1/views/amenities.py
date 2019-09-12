#!/usr/bin/python3
''' Routes for amenity objects '''
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    ''' get all amenity objs '''
    data = storage.all('Amenity')
    new = [val.to_dict() for key, val in data.items()]
    return jsonify(new)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    ''' returns an individual amenity object '''
    obj = storage.get('Amenity', amenity_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    ''' deletes an individual amenity '''
    obj = storage.get('Amenity', amenity_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404)

    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    ''' create an amenity if doesn't already exist '''
    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in args:
        return jsonify({"error": "Missing name"}), 400
    obj = Amenity(**args)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    ''' updates an individual amenity '''
    obj = storage.get('Amenity', amenity_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404)
    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in args.items():
        if k not in ["id", "updated_at", "created_at"]:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict())
