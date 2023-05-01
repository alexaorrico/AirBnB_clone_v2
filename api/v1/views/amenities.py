#!/usr/bin/python3

"""This is the Views for Amenity Class Objects"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def amenity_object(amenity_id=None):
    """ A Function that performs CRUD for State Class"""

    my_amenities = storage.all(Amenity)

    amenities = [items.to_dict() for items in my_amenities.values()]
    if not amenity_id:
        if request.method == 'GET':
            return jsonify(amenities)
        elif request.method == 'POST':
            my_dict = request.get_json()

            if my_dict is None:
                abort(400, 'Not a JSON')
            if my_dict.get("name") is None:
                abort(400, 'Missing Name')
            new_amenity = Amenity(**my_dict)
            new_amenity.save()
            return jsonify(new_amenity.to_dict()), 201

    else:
        if request.method == 'GET':
            for amen in amenities:
                if amen.get('id') == amenity_id:
                    return jsonify(amenities)
            abort(404)

        elif request.method == 'PUT':
            my_dict = request.get_json()

            if my_dict is None:
                abort(400, 'Not a JSON')
            for amen in my_amenities.values():
                if amen.id == amenity_id:
                    amen.name = my_dict.get('name')
                    amen.save()
                    return jsonify(amen.to_dict()), 200
            abort(404)

        elif request.method == 'DELETE':
            for obj in my_amenities.values():
                if obj.id == amenity_id:
                    storage.delete(obj)
                    storage.save()
                    return jsonify({}), 200
            abort(404)
