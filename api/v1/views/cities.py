from api.v1.views import app_views
from flask import jsonify, abort, make_response,request
from flasgger.utils import swag_from
from models import storage
from models.state import State
from models.city import City

@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/city/cities_by_state.yml', methods=['GET'])
def cities_by_states(state_id):
    city_list = []
    states = storage.get(State, state_id)
    if not states:
        abort(404)

    for cities in states.cities:
        city_list.append(cities.to_dict())
    
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/get_city.yml', methods=['GET'])
def cities(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())
 

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/city/delete_city.yml', methods=['DELETE'])
def delete_city(city_id):
     city = storage.get(City, city_id)
     if not city:
          abort(404)
    
     storage.delete(city)
     storage.save()

     return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/city/create_city.yml', methods=['POST'])
def create_city(state_id):
     state = storage.get(State, state_id)
     if not state:
          abort(404)

     request_data = request.get_json
     if not request_data:
          abort(400, description='Not a JSON')
     if 'name' not in request_data:
          abort(400, description='Missing name')

     city = City(**request_data)
     city.state_id = state.id
     city.save()

     return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/city/update_city.yml', methods=['PUT'])
def update_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    request_data = request.get_json
    if not request_data:
        abort(400, description='Not a JSON')

    ignored_fields = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in request_data.items():
        if key not in ignored_fields:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
