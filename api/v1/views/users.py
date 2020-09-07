#!/usr/bin/python3

from models.base_model import *
from api.v1.views import app_views
from models import storage
from models.user import *
from flask import jsonify, abort, request, make_response
    

@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def users():
    ls = []
    users = storage.all('User')
    if request.method == "GET":
        for key, value in users.items():
            ls.append(value.to_dict())
        return jsonify(ls)
    elif request.method == "POST":
        if not request.json:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        elif not 'email' in request.json:
            return make_response(jsonify({'error': "Missing email"}), 400)
        elif not 'password' in request.json:
            return make_response(jsonify({'error': "Missing password"}), 400)
        else:
            new = User(**request.json)
            new.save()
            return make_response(new.to_dict(), 201)
           


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def user(user_id):
    users = storage.all('User')
    for key, value in users.items():
        if user_id == value.id:
            if request.method == "GET":
                return value.to_dict()
            elif request.method == "DELETE":
                storage.delete(value)
                storage.save()
                return {}
            elif request.method == "PUT":
                if not request.json:
                    return make_response(jsonify({'error': "Not a JSON"}), 400)
                else:
                    json = request.json
                    for key2, value2 in json.items():
                        if key2 != 'id' and key != 'email' and key2 != 'created_at' and key2 != "updated_at":
                            setattr(value, key2, value2)
                    value.updated_at = datetime.utcnow() 
                    storage.save()
                    return make_response(value.to_dict(), 200)
    abort(404)
