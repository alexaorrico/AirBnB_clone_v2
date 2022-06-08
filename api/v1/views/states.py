#!/usr/bin/python3
"""states api"""
from flask import abort, jsonify, request, make_response
from models import storage
from models.engine.db_storage import classes
from api.v1.views import app_views


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def state_view(state_id=None):
    """state view"""
    if state_id:
        state_obj = storage.get(classes["State"], state_id)
        # print("{}".format(state_obj))

        if not state_obj:
                abort(404)

        if request.method == "GET":
            state_obj = state_obj.to_dict()
            return jsonify(state_obj)

        elif request.method == "DELETE":
            state_obj.delete()
            storage.save()
            return jsonify({})

        elif request.method == "PUT":
            try:
                obj_json = request.get_json()
            except:
                return jsonify({"error": "Not found"}), 400

            for key, value in obj_json.items():
                if key not in ["updated_at", "id", "created_at"]:
                    setattr(state_obj, key, value)

            state_obj.save()

            state_obj = state_obj.to_dict()
            return jsonify(state_obj), 200

    else:

        if request.method == "GET":
            states_list = []
            states = storage.all(classes["State"])
            for k, v in states.items():
                states_list.append(v.to_dict())
            return jsonify(states_list)

        else:
            # falsee = request.is_json()
            # if  not falsee:
            #     return jsonify({"error": "Not a JSON"}), 400

            obj_json = request.get_json()

            if "name" not in obj_json.keys():
                return jsonify({"error": "Missing name"}), 400

            new_state = classes["State"](name = obj_json["name"])
            new_state.save()

            new_state_dict = new_state.to_dict()
            return jsonify(new_state_dict), 201