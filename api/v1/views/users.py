#!/usr/bin/python3
"""users api"""


from api.v1.views import app_views
from models.engine.db_storage import classes
from models import storage
from flask import jsonify, abort, request

@app_views.route("/users", methods=["GET", "POST"])
@app_views.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"])
def users_view(user_id=None):
    if user_id:
        user_obj = storage.get(classes["User"], user_id)
        if not user_obj:
            abort(404)

        if request.method == "GET":
            user_obj = user_obj.to_dict()
                
            return jsonify(user_obj)
        elif request.method == "PUT":
            try:
                obj_json = request.get_json()
            except:
                return jsonify({"error": "Not found"}), 400

            for key, value in obj_json.items():
                if key not in ["updated_at", "id", "created_at", "email"]:
                    setattr(user_obj, key, value)

            user_obj.save()

            user_obj = user_obj.to_dict()
            return jsonify(user_obj), 200
        elif request.method == "DELETE":
            user_obj.delete()
            storage.save()

            return jsonify({})
    else:
        if request.method == "GET":
            users_list = []
            users = storage.all(classes["User"])
            for k, v in users.items():
                users_list.append(v.to_dict())
            return jsonify(users_list)

        else:
            # falsee = request.is_json()
            # if  not falsee:
            #     return jsonify({"error": "Not a JSON"}), 400

            obj_json = request.get_json()

            if "email" not in obj_json.keys():
                return jsonify({"error": "Missing name"}), 400

            if "password" not in obj_json.keys():
                return jsonify({"error": "Missing password"}), 400

            new_user = classes["User"](first_name = obj_json.get("first_name"), 
                                            last_name = obj_json.get("last_name"), 
                                            email = obj_json.get("email"),
                                            password = obj_json.get("password"))
            new_user.save()

            new_user_dict = new_user.to_dict()
            return jsonify(new_user_dict), 201
