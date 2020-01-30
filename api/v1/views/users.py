#!/usr/bin/python3
'''
API for User
'''
from models.user import User
from models import storage
from flask import Flask, abort, jsonify, request, json
from api.v1.views import app_views


@app_views.route('/users/', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def all_user(user_id=None):
    '''Returns all or an user object in JSON'''
    json_list = []
    try:
        if user_id is None:
            for v in storage.all('User').values():
                json_list.append(v.to_dict())
        else:
            json_list = storage.get('User', user_id).to_dict()
        return jsonify(json_list)
    except Exception:
        abort(404)


def attrib_update(obj, **args):
    '''Update objects to correct types'''
    for key, value in args.items():
        if hasattr(obj, key):
            value = value.replace("_", " ")
            try:
                value = eval(value)
            except Exception:
                pass
            setattr(obj, key, value)


@app_views.route('/users/', methods=['POST'])
def create_user():
    '''Creates an instance of User'''
    form = request.get_json(force=True)
    if 'password' not in request.json:
        return jsonify({"error": "Missing password"}), 400
    if 'email' not in request.json:
        return jsonify({"error": "Missing email"}), 400
    user_class = models.classes['User']
    new_user = user_class()
    attrib_update(new_user, **form)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    '''Deletes an user object'''
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404)
    else:
        storage.delete(user_obj)
        storage.save()
    return jsonify({})


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    '''Updates User object attribute'''
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404)
    form = request.get_json(force=True)
    for k, v in form.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(user_obj, k, v)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
