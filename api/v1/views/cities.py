#!/usr/bin/python3
"""
New view for class State
To handle all default Restful API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def states_state_id_cities(state_id):
    """Retrieves all City objects of a State"""

    state_catch = storage.get('State', state_id)

    # If the state_id is not linked to any State object, raise a 404 error
    if state_catch is None:
        abort(404)

    # retrieves City object
    if request.method == 'GET':
        cities = storage.all(City)
        cities_list = []
        for city in cities.values():
            cities_dict = city.to_dict()
            if cities_dict['state_id'] == state_id:
                cities_list.append(cities_dict)
        return jsonify(cities_list)
    
        elif request.method == 'POST':
        # transform the HTTP body request to a dictionary
        body_request_dict = request.get_json()

        # If the HTTP body request is not valid JSON
        if not body_request_dict:
            abort(400, 'Not a JSON')

        # If the dictionary doesn’t contain the key name
        if 'name' not in body_request_dict:
            abort(400, 'Missing name')

        # create new object State with body_request_dict
        body_request_dict['state_id'] = state_id
        new_city = City(**body_request_dict)

        storage.new(new_city)
        storage.save()
        return new_city.to_dict(), 

# @app_views.route('/states/<state_id>', methods=['GET'])
# def pick_state_obj(state_id):
#     """Retrieves a `State` object/Error if no linkage to any id"""
#     state_pick = storage.get("State", state_id)
#     if state_pick is None:
#         # use abort to return 404
#         # in the middle of a route
#         abort(404)
#     return jsonify(state_pick.to_dict())


# @app_views.route('/states/<state_id>', methods=['DELETE'])
# def delete_state(state_id):
#     """
#     Deletes a `State`object based on its id
#     Raise error if no linkage found
#     """
#     state_rm = storage.get("State", state_id)
#     if state_rm is None:
#         abort(404)
#     state_rm.delete()
#     storage.save()
#     return jsonify({}), 200


# @app_views.route('/states/', methods=['POST'])
# def post_state():
#     """Method to create a `State` object"""
#     json_data = request.get_json()
#     if not json_data:
#         abort(400, 'This is not JASON!!')
#     elif 'name' not in json_data:
#         abort(400, 'Missing name')
#     new_post = State(name=json_data['name'])
#     new_post.save()
#     return jsonify(new_post.to_dict()), 200


# @app_views.route('/states/<state_id>', methods=['PUT'])
# def upd_state(state_id):
#     """
#     Update a `State` object
#     Error if no linkage found
#     """
#     json_data = request.get_json()
#     if not json_data:
#         abort(400, 'This is not JASON!!')

#     state_upd = storage.get("State", state_id)
#     if state_upd is None:
#         abort(404)
#     state_upd.name = json_data['name']
#     state_upd.save()
#     return jsonify(state_upd.to_dict()), 200
