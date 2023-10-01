# #!/usr/bin/python3
# """
#     module cities
# """

# import models
# from models import storage
# from models.state import *
# from models.city import *

# from flask import Flask, jsonify, abort, request
# from api.v1.views import app_views


# @app_views.route('/cities', methods=['GET'], strict_slashes=False)
# def get_cities():
#     """
#         A function that Retrieves the list of all
#         City objects: GET /api/v1/cities
#     """
#     # get all saved state objects
#     cities = storage.all(City).values()

#     # Convert state object to dictionary and save in list
#     stateList = [state.to_dict() for state in cities]

#     return jsonify(stateList)


# @app_views.route('/cities/<state_id>', methods=['GET'], strict_slashes=False)
# def get_state(state_id):
#     """
#         A function that Retrieves the list of all
#         City objects: GET /api/v1/cities
#     """
#     obj = storage.get(City, state_id)

#     if (obj):
#         return jsonify(obj.to_dict())
#     else:
#         abort(404)


# @app_views.route('/cities/<state_id>', methods=['DELETE'], strict_slashes=False)
# def del_state(state_id):
#     """
#         A function that Deletes a City object:
#         DELETE /api/v1/cities/<state_id>
#     """
#     obj = storage.get(City, state_id)

#     # delete and save if state object is found, if not return error 404
#     if (obj):
#         storage.delete(obj)
#         storage.save()
#         return jsonify({}), 200
#     else:
#         abort(404)


# @app_views.route('/cities', methods=['POST'], strict_slashes=False)
# def add_state():
#     """
#         A function that Creates a City:
#         POST /api/v1/cities
#     """
#     json_str = request.get_json()

#     # Check If the HTTP body request is not valid JSON
#     if (not json_str):
#         abort(400, 'Not a JSON')
#     if ('name' not in json_str):
#         abort(404, 'Missing name')

#     # create a new state object, save and return it
#     obj = City(**json_str)
#     obj.save()

#     return jsonify(obj.to_dict()), 201


# @app_views.route('/cities/<state_id>', methods=['PUT'], strict_slashes=False)
# def update_state(state_id):
#     """
#         A function that Updates a City object:
#         PUT /api/v1/cities/<state_id>
#     """
#     obj = storage.get(City, state_id)
#     if (not obj):
#         abort(404)

#     json_str = request.get_json()
#     # Check If the HTTP body request is not valid JSON
#     if (not json_str):
#         abort('400', 'Not a JSON')
    
#     # Update state object attributes
#     to_ignore = ['id', 'created_at', 'updated_at']
#     for key, value in json_str.items():
#         if key not in to_ignore:
#             setattr(obj, key, value)

#     #  save and return
#     obj.save()

#     return jsonify(obj.to_dict()), 200
