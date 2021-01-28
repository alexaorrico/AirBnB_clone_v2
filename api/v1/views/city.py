"""City module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def states(state_id=None):
    """ xd """

    data = storage.get(State, state_id)
    if data is None:
        abort(404)

    cities = []
    for city in data.cities:
        cities.append(city.dict())
    return jsonify(cities)