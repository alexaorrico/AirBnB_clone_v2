# #!/usr/bin/python3
# """
# cities.py
# """
# from . import app_views
# from flask import jsonify
# from models import storage
# from models.city import City
# from models.state import State
# from flask import abort, request, Response, make_response
# import json


# @app_views.route('states/<state_id>/cities',
#                  methods=['GET'], strict_slashes=False)
# def cities_per_id(state_id):
#     """
#     Retrieves the list of all City
#     objects of a State
#     """
#     desired_cities = []
#     for key, value in storage.all(City).items():
#         if value.state_id == state_id:
#             desired_cities.append({key: value})
#     if desired_cities != []:
#         return jsonify(desired_cities)
#     else:
#         abort(404)


# @app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
# def city_by_id(city_id):
#     """
#     retrieves one city per id
#     """
#     city = storage.get(City, city_id)
#     if city:
#         return jsonify(city.to_dict()), 200
#     else:
#         abort(404)


# @app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
# def delete_city(city_id):
#     """
#     deletes city
#     """
#     city = storage.get(City, city_id)
#     if city:
#         storage.delete(city)
#         storage.save()
#         return jsonify({}), 200
#     else:
#         abort(404)


# @app_views.route('states/<state_id>/cities',
#                  methods=['POST'], strict_slashes=False)
# def POST_city(state_id):
#     """
#     add city
#     """
#     if not storage.get(State, state_id):
#         abort(404)
#     data = request.get_json()
#     if not data:
#         abort(400, 'Not a JSON')
#     if 'name' not in data:
#         abort(400, 'Missing name')

#     new_city = City(**data)
#     setattr(new_city, "state_id", state_id)
#     new_city.save()
#     return jsonify(new_city.to_dict()), 201


# @app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
# def put_city(city_id):
#     """
#     updates city
#     """
#     city_to_be_updated = storage.get(City, city_id)
#     if not city_to_be_updated:
#         abort(404)
#     data = request.get_json()
#     if not data:
#         abort(400, 'Not a JSON')
#     ignored_keys = ['id', 'updated_at', 'created_at']
#     for key, value in data.items():
#         if key in ignored_keys:
#             continue
#         setattr(city_to_be_updated, key, value)
#     city_to_be_updated.save()
#     return jsonify(city_to_be_updated.to_dict()), 200


#!/usr/bin/python3
""" return dict repersantation of object """
from models import storage
from models.engine.db_storage import classes
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def city_get(state_id):
    result = []
    """ get all the city objects in a state """
    state = storage.get(classes["State"], state_id)
    if not state:
        abort(404)
    for i in state.cities:
            result.append(i.to_dict())
    return jsonify(result)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def city_specific(city_id):
    """ get the specific object from city """
    city = storage.get(classes["City"], city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def city_specific_delete(city_id):
    """ delete the inputed object from city """
    task = [task for task in storage.all(
        "City").values() if task.id == city_id]
    if len(task) == 0:
        abort(404)
    storage.delete(task[0])
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 methods=['POST'], strict_slashes=False)
def city_specific_post(state_id):
    """ post the inputed object from city with state_id """
    if not request.json:
        return make_response("Not a JSON", 400)
    if 'name' not in request.json:
        return make_response("Missing name", 400)
    obj = classes["City"]
    try:
        new_item = obj()
        setattr(new_item, "state_id", state_id)
        setattr(new_item, "name", request.json["name"])
        new_item.save()
        return new_item.to_dict(), 201
    except BaseException:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def city_specific_put(city_id):
    """ update the specific object from city with city_id """
    instance = None
    if not request.json:
        return make_response("Not a JSON", 400)
    check = ["id", "created_at", "updated_at", "state_id"]
    for i in storage.all("City").values():
        if i.id == city_id:
            instance = i
            for key, value in request.json.items():
                if key not in check:
                    setattr(i, key, value)
                    i.save()
    if not instance:
        abort(404)
    return instance.to_dict(), 200
