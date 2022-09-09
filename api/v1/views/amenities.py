#!/usr/bin/python3
"""file amenities"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort
import json


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def amenities(amenity_id=None):
    """Function to return all amenities objects"""
    if request.method == "GET":
        if amenity_id is None:
            list_of_amenities = []
            amenities = storage.all(Amenity)
            for key, value in amenities.items():
                obj = value.to_dict()
                list_of_amenities.append(obj)
            return jsonify(list_of_amenities)
        else:
            amenities = storage.all(Amenity)
            for key, value in amenities.items():
                if amenities[key].id == amenity_id:
                    return jsonify(value.to_dict())
            abort(404)
    elif request.method == 'DELETE':
        amenities = storage.all()
        for key, value in amenities.items():
            if amenities[key].id == amenity_id:
                storage.delete(amenities[key])
                storage.save()
                return jsonify({}), 200
        abort(404)
    elif request.method == 'POST':
        try:
            body = request.get_json()
            if 'name'in body:
                value = {}
                value['name'] = body['name']
                new_amenity = Amenity(**value)
                new_amenity.save()
                return jsonify(new_amenity.to_dict()), 201
            else:
                return jsonify({
                    "error": "Missing name"
                }), 400
        except Exception as error:
            return jsonify({
                    "error": "Not a JSON"
                }), 400
    else:
        try:
            notAttr = ['id', 'created_at', 'updated_at']
            body = request.get_json()
            amenities = storage.all(Amenity)
            for key, value in amenities.items():
                if amenities[key].id == amenity_id:
                    for k, v in body.items():
                        if k not in notAttr:
                            setattr(value, k, v)
                    value.save()
                    return jsonify(value.to_dict()), 200
            return jsonify({"error": "Not found"}), 404
        except Exception as error:
            return jsonify({
                "error": "Not a JSON"
            }), 400
