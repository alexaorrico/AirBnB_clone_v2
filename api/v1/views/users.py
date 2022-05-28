#!/usr/bin/python3
"""
-------------------
New view for States
-------------------
"""
from models.user import User
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from api.v1.views.aux_func import aux_func


methods = ["GET", "DELETE", "POST", "PUT"]


@app_views.route("/users", methods=methods)
@app_views.route("/users/<user_id>", methods=methods)
def users(user_id=None):
    """
    ---------------
    Route for Users
    ---------------
    """
    users = storage.all(User)
    met = request.method
    if met in ["GET", "DELETE"]:
        res = aux_func(User, met, user_id)
        return res
    if met == 'POST':
        try:
            data_user = request.get_json()
            if "email" not in data_user.keys():
                return jsonify("Missing email"), 400, {'ContentType':
                                                       'application/json'}
            elif "password" not in data_user.keys():
                return jsonify("Missing password"), 400, {'ContentType':
                                                          'application/json'}
            else:
                new_user = User(**data_user)
                # No sabemos si hay que guardar
                new_user.save()
                return jsonify(new_user.to_dict()), 201, {'ContentType':
                                                          'application/json'}
        except Exception as err:
            return jsonify("Not a JSON"), 400, {'ContentType':
                                                'application/json'}
    elif request.method == "PUT":
        if user_id:
            key = "User.{}".format(user_id)
            if key not in users.keys():
                abort(404)
            else:
                try:
                    data_user = request.get_json()
                    user = users[key]
                    for attr, value in data_user.items():
                        if attr not in ["id", "created_at", "updated_at",
                                        "email"]:
                            setattr(user, attr, value)
                    # No sabemos si hay que guardar
                    storage.save()
                    return jsonify(user.to_dict()), 201, {'ContentType':
                                                          'application/json'}
                except Exception as err:
                    return jsonify("Not a JSON"), 400, {'ContentType':
                                                        'application/json'}
