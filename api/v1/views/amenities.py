#!/usr/bin/python3
""" API REST for Amenity """
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities')
def amenities_all():
    """ Route return all amenities """
    return jsonify(list(map(lambda x: x.to_dict(),
                            list(storage.all(Amenity).values()))))


@app_views.route('/amenities/<amenity_id>')
def amenities_id(amenity_id):
    """ Route return amenities with referenced id """
    my_amenity = storage.get('Amenity', amenity_id)
    try:
        return jsonify(my_amenity.to_dict())
    except:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenities_id(amenity_id):
    """ Route delete amenities with referenced id """
    my_object = storage.get('Amenity', amenity_id)
    if my_object is not None:
        storage.delete(my_object)
        storage.save()
    else:
        abort(404)
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenities():
    """ Route create amenities """
    if request.is_json:
        try:
            data = request.get_json()
            if 'name' in data:
                new_amenity = Amenity(**data)
                new_amenity.save()
                return jsonify(new_amenity.to_dict()), 201
            else:
                return jsonify(error="Missing name"), 400
        except:
            return jsonify(error="Not a JSON"), 400
    else:
        return jsonify(error="Not a JSON"), 400


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenities(amenity_id):
    """ Route update amenities """
    if request.is_json:
        try:
            data = request.get_json()
            my_object = storage.get('Amenity', amenity_id)
            if my_object is not None:
                for keys, values in data.items():
                    if keys not in ["created_at", "updated_at", "id"]:
                        setattr(my_object, keys, values)
                my_object.save()
                return jsonify(my_object.to_dict()), 200
            else:
                abort(404)
        except:
            return jsonify(error="Not a JSON"), 400
    else:
        return jsonify(error="Not a JSON"), 400
