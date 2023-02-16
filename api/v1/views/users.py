
#!/usr/bin/python3
""" User APIRest
"""

from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'])
def user_list():
    """ list of an objetc in a dict form
    """
    lista = []
    dic = storage.all('User')
    for elem in dic:
        lista.append(dic[elem].to_dict())
    return (jsonify(lista))


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE'])
def user_id(user_id):
    """ realize the specific action depending on method
    """
    lista = []
    dic = storage.all('User')
    for elem in dic:
        var = dic[elem].to_dict()
        if var["id"] == user_id:
            if request.method == 'GET':
                return (jsonify(var))
            elif request.method == 'DELETE':
                aux = {}
                dic[elem].delete()
                storage.save()
                return (jsonify(aux))
    abort(404)


@app_views.route('/users', methods=['POST'])
def user_item():
    """ add a new item
    """
    if not request.json:
        return jsonify("Not a JSON"), 400
    else:
        content = request.get_json()
        if "email" not in content.keys():
            return jsonify("Missing email"), 400
        if "password" not in content.keys():
            return jsonify("Missing password"), 400
        else:
            new_user = User(**content)
            new_user.save()
            return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ update an item
    """
    dic = storage.all("User")
    for key in dic:
        if dic[key].id == user_id:
            if not request.json:
                return jsonify("Not a JSON"), 400
            else:
                forbidden = ["id", "email", "update_at", "created_at"]
                content = request.get_json()
                for k in content:
                    if k not in forbidden:
                        setattr(dic[key], k, content[k])
                dic[key].save()
                return(jsonify(dic[key].to_dict()))
    abort(404)
