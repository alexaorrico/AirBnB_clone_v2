#!/usr/bin/python3
""" Amenities main file """

from flask import request, jsonify, abort, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


def create(new_data, old_data=None):
    """ Create an existence object """
    try:
        values = {}
        new_amenity = Amenity()

        if (old_data is None):
            if 'name' not in new_data:
                abort(400, description='Missing name')

            for key, value in new_data.items():
                setattr(new_amenity, key, value)

        else:

            for key, value in old_data.items():
                setattr(new_amenity, key, value)

            for key, value in new_data.items():
                if key != 'id' and key != 'created_at' and key != 'updated_at':
                    setattr(new_amenity, key, value)

        for key, value in new_amenity.to_dict().items():
            values[key] = value

        new_amenity.save()

        return jsonify(values)

    except Exception:
        abort(400, description='Not a JSON')


def delete(amenity_id, update_flag=0):
    """ Delete an existence object """
    try:
        amenity = storage.get(Amenity, amenity_id)

        if amenity is None:
            raise Exception

        storage.delete(amenity)
        storage.save()

        return make_response({}, 200)

    except Exception:
        abort(404)


def show(amenity_id=None):
    """ show an existence object/s """
    all_amenities = []
    values = {}
    if amenity_id is None:
        for string, amenity_item in storage.all('Amenity').items():
            new_amenity = {}
            for key, value in amenity_item.to_dict().items():
                new_amenity[key] = value

            all_amenities.append(new_amenity)

        return jsonify(all_amenities)

    else:
        try:
            for key, value in storage.get(Amenity, amenity_id).to_dict().items():
                values[key] = value

            return jsonify(values)
        except Exception:
            abort(404)


def update(amenity_id, new_data):
    """ Update an existence object """
    values = {}
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    try:
        for key, value in new_data.items():
            if (key != 'id' and key != 'created_at' and key != 'updated_at'):
                setattr(amenity, key, value)

        for key, value in amenity.to_dict().items():
            values[key] = value

        amenity.save()

        return jsonify(values)

    except Exception:
        abort(400, description='Missing name')


@app_views.route('/amenities/', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """ Getting all the amenities or creating a new amenity """
    if request.method == 'GET':
        return show()
    else:
        new_data = request.get_json()
        return create(new_data)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def amenity(amenity_id):
    """ A selected amenity """
    if request.method == 'GET':
        return show(amenity_id)

    elif request.method == 'DELETE':
        return delete(amenity_id, update_flag=0)

    else:
        new_data = request.get_json()
        return update(amenity_id, new_data)
