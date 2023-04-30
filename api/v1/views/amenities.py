#!/usr/bin/python3
'''
amenities handler
'''
from flask import Flask, make_response, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'])
def all_amenities():
    if request.method == 'GET':
        return jsonify([amen.to_dict()
                        for amen in storage.all('Amenity').values()])
    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        new_amen = Amenity(**request.get_json())
        new_amen.save()
        return make_response(jsonify(new_amen.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity(amenity_id):

    amen = storage.get('Amenity', amenity_id)

    if not amen:
        abort(404)

    if request.method == 'GET':
        return make_response(jsonify(amen.to_dict()), 200)

    if request.method == 'DELETE':
        storage.delete(amen)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amen, key, value)
        amen.save()
        return make_response(jsonify(amen.to_dict()), 200)
