#!/usr/bin/python3
"""
    HBNB_V3: Task 10
"""
from api.v1.views.index import app_views, User
from models import storage
from flask import jsonify, request, abort


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def viewalltheuserthings():
    """Retrieves the list of all User objects"""

    if request.method == 'GET':
        utl = storage.all(User)
        li = []
        for user in utl.values():
            li.append(user.to_dict())
        return jsonify(li)
    if request.method == 'POST':
        try:
            body = request.get_json()
            if "email" not in body.keys():
                return "Missing email", 400
            elif "password" not in body.keys():
                return "Missing password", 400
            else:
                newuser = User(**body)
                """for k in body.keys():
                    setattr(newstate, k, body.get(k))"""
                """newstate.__dict__.update(body)"""
                newuser.save()
                return jsonify(newuser.to_dict()), 201

        except:
            abort(400, "Not a JSON")


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def useridtime(user_id):
    """Handles an user object with said id depending on HTTP request"""
    utl = storage.all(User)
    k = "User." + user_id
    if k in utl.keys():
        u = utl.get(k)
        ud = u.to_dict()
        if request.method == 'GET':
            return jsonify(ud)
        if request.method == 'DELETE':
            storage.delete(u)
            storage.save()
            return jsonify({})
        if request.method == 'PUT':
            try:
                body = request.get_json()
                body.pop("id", "")
                body.pop("created_at", "")
                body.pop("updated_at", "")
                body.pop("email", "")
                """s.__dict__.update(body)"""
                for k in body.keys():
                    setattr(u, k, body.get(k))
                """s.save()"""
                u.save()
                ud = u.to_dict()
                return jsonify(ud)

            except:
                abort(400, "Not a JSON")

    else:
        abort(404)
