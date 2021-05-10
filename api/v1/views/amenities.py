#!/usr/bin/python3
'''Creates routes that handles states with JSON'''
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities_manage():
    '''returns list of users or creates new one'''
    if request.method == 'POST':
        try:
            content = request.get_json()
            if content is None:
                abort(400, 'Not a JSON')
        except Exception as e:
            abort(400, 'Not a JSON')
        if 'email' not in content.keys():
            abort(400, 'Missing email')
        if 'password' not in content.keys():
            abort(400, 'Missing password')
        new_instance = User(password=content['password'],
                            email=content['email'])
        new_instance.save()
        return jsonify(new_instance.to_dict()), 201
    else:
        user_list = []
        for user_obj in storage.all("User").values():
            user_list.append(user_obj.to_dict())
        return jsonify(user_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def amenity_specific(amenity_id):
    '''manages specific state object'''
    amenity_target = storage.get(Amenity, amenity_id)
    if amenity_target is None:
        abort(404)
    if request.method == 'PUT':
        try:
            content = request.get_json()
            if content is None:
                abort(400, 'Not a JSON')
        except Exception as e:
            abort(400, 'Not a JSON')
        ignore = ['id', 'email', 'created_at', 'updated_at']
        for key, val in content.items():
            if key not in ignore:
                setattr(amenity_target, key, val)
        amenity_target.save()
        return jsonify(amenity_target.to_dict())
    elif request.method == 'DELETE':
        storage.delete(amenity_target)
        storage.save()
        return jsonify({})
    else:
        return jsonify(amenity_target.to_dict())
