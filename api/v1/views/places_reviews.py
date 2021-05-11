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


@app_views.route('/reviews', methods=['GET', 'POST'], strict_slashes=False)
def reviews_manage():
    '''returns list of reviews or creates new one'''
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
        new_instance = review(password=content['password'],
                            email=content['email'])
        new_instance.save()
        return jsonify(new_instance.to_dict()), 201
    else:
        review_list = []
        for review_obj in storage.all("review").values():
            review_list.append(review_obj.to_dict())
        return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def review_specific(review_id):
    '''manages specific state object'''
    review_target = storage.get(review, review_id)
    if review_target is None:
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
                setattr(review_target, key, val)
        review_target.save()
        return jsonify(review_target.to_dict())
    elif request.method == 'DELETE':
        storage.delete(review_target)
        storage.save()
        return jsonify({})
    else:
        return jsonify(review_target.to_dict())
