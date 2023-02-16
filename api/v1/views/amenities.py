#!/usr/bin/python3
"""
Views for Amenity model
"""
from api.v1.views import app_views
from flask import abort, jsonify, request

from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'])
@app_views.route('/amenities/<id>', methods=['GET', 'PUT', 'DELETE'])
def amenities(id=None):
    """Amenity model view"""
    if request.method == 'GET':
        if id:
            obj = storage.get(Amenity, id)
            if not obj:
                abort(404)
            return jsonify(obj.to_dict())
        else:
            objs = [obj.to_dict() for obj in storage.all(Amenity).values()]
            return jsonify(objs)

    elif request.method == 'DELETE':
        obj = storage.get(Amenity, id)
        if not obj:
            abort(404)
        obj.delete()
        storage.save()
        return jsonify({})

    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({'error': 'Not a JSON'}), 400
        data = request.get_json()
        if not data.get('name'):
            return jsonify({'error': 'Missing name'}), 400
        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201

    elif request.method == 'PUT':
        obj = storage.get(Amenity, id)
        if not obj:
            abort(404)
        if not request.is_json:
            return jsonify({'error': 'Not a JSON'}), 400
        data = request.get_json()
        for k, v in data.items():
            if k != 'id' and k != 'created_at' and k != 'updated_at':
                setattr(obj, k, v)
        obj.save()
        return jsonify(obj.to_dict())
