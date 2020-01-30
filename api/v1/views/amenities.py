#!/usr/bin/python3
"""Flask app to handle amenities API"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'])
def get_amenity():
    """Retrun a list of all amenities"""
    amenities_dict = storage.all('Amenity')
    amenities_list = [am.to_dict() for am in amenities_dict.values()]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """Retrun an  amenity"""
    amenities_dict = storage.all('Amenity')
    amenities_list = [am.to_dict() for am in amenities_dict.values()
                      if am.id == amenity_id]
    if len(amenities_list) == 0:
        abort(404)
    return jsonify(amenities_list[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_amenity_by_id(amenity_id):
    """Deletes an Amenity"""
    am_to_erase = storage.get("Amenity", amenity_id)
    if am_to_erase is None:
        abort(404)
    am_to_erase.delete()
    storage.save()
    erased = {}
    return jsonify(erased)


@app_views.route('/amenities', methods=['POST'])
def post_amenity():
    """creates an Amenity"""
    am_attr_dict = request.get_json()
    if not request.json:
        return jsonify("Not a JSON"), 400
    if 'name' not in am_attr_dict:
        return jsonify("Missing name"), 400
    new_am = Amenity(**am_attr_dict)
    new_am.save()
    am = new_am.to_dict()
    return jsonify(am), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updates_amenity(amenity_id):
    """uptes an Amenity"""
    am = storage.get("Amenity", amenity_id)
    if am is None:
        abort(404)
    am_attr_dict = request.get_json()
    if not request.json:
        return jsonify("Not a JSON"), 400
    ignore = ["id", "update_at", "created_at"]
    for key, value in am_attr_dict.items():
        if key not in ignore:
            setattr(am, key, value)
    am.save()
    new_am = am.to_dict()
    return jsonify(new_am)
