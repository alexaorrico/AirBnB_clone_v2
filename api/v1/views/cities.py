# #!/usr/bin/python3
# """a new view for City objects that handles all default RESTFul
# API actions"""
# from api.v1.views import app_views
# from models.state import State
# from models.city import City
# from models import storage
# from flask import Flask, jsonify, abort, make_response, request
# from sqlalchemy.exc import IntegrityError


# @app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
# def all_cities(state_id):
#     """Retrieves the list of all City objects of a State"""
#     state = storage.get(State, state_id)
#     if state is None:
#         abort (404)
#     cities_list = [city.to_dict() for city in state.cities]
#     return jsonify(cities_list)


# @app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
# def id_state(city_id):
#     city = storage.get(City, city_id)
#     if city is None:
#         abort (404)
#     return jsonify(city.to_dict())


# @app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
# def delete(state_id):
#     try:
#         state = storage.get(State, state_id)
#         if state is None:
#             abort (404)
#         storage.delete(state)
#         storage.save()
#         return make_response(jsonify({}), 200)
#     except IntegrityError:
#         return jsonify(error=True, message="Invalid state_id provided"), 400


# @app_views.route('/states', methods=['POST'], strict_slashes=False)
# def post():
#     dict = request.get_json()
#     if dict is None:
#         abort (400, 'Not a JSON')
#     if dict.get('name') is None:
#         abort (400, 'Missing name')
#     new_status = State(**dict)
#     storage.save()
#     return make_response(jsonify(new_status.to_dict()), 201)


# @app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
# def put(state_id):
#     state = storage.get(State, state_id)
#     if state is None:
#         abort (404)
#     dict = request.get_json()
#     if dict is None:
#         abort (400, 'Not a JSON')
#     keys_substract = ['id', 'created_at', 'updated_at']
#     for key, val in dict.items():
#         if key not in keys_substract:
#             setattr(state, key, val)
#     storage.save()
#     return (jsonify(state.to_dict()), 200)
