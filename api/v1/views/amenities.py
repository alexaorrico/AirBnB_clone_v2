#!/usr/bin/python3
""" functions GET, PUT, POST & DELETE """

from flask import jsonify, request, abort
from api.v1.views import app_views
from models.amenities import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'])
def get_all():
    """ get all the states """
    new = []
    amenity = storage.all(Amenity)
    for i in amenity:
        new.append(amenity[i].to_dict())
    return jsonify(new)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_id(amenity_id):
    """ get status by id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict()), 200
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def del_id(amenity_id):
    """ delete state by id """
    amenity = storage.get(Amenity, amenity_id)
    storage.delete(Amenity)
    storage.save()
    if not amenity:
        abort(404)
    return ({}), 200


@app_views.route('/amenities', methods=['POST'])
def add():
    """ add statte to storage """
    if request.json:
        content = request.get_json()
        if "name" not in content.keys():
            return jsonify("Missing name"), 400
        else:
            add_amenity = Amenity(**content)
            add_amenity.save()
            return jsonify(add_amenity.to_dict()), 201
    return jsonify("Not a JSON"), 400


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update(amenity_id):
    """ update states with id """
    dic = storage.all(Amenity)
    for i in dic:
        if dic[i].id == amenity_id:
            if request.json:
                ignore = ["id", "created_at", "updated_at"]
                content = request.get_json()
                for items in content:
                    if items not in ignore:
                        setattr(dic[i], items, content[items])
                dic[i].save()
                return jsonify(dic[i].to_dict())
            else:
                return jsonify("Not a JSON"), 400
    abort(404)
