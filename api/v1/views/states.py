#!/usr/bin/python3
# Index
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/states/<state_id>', methods=['GET','DELETE'])
@app_views.route('/states', methods=['GET'])
def states(state_id=None):
    """def function que devuelve una lista de todos los State"""
    lista_states = []
    if request.method == 'GET':
        if state_id is None:
            states = storage.all(State)
            for key,value in states.items():
                obj = value.to_dict()
                lista_states.append(obj)
            return jsonify(lista_states)
        else:
            states = storage.all(State)
            for key,value in states.items():
                if states[key].id == state_id:
                    return jsonify(value.to_dict())
            abort(404)
    else:
        states = storage.all()
        for key,value in states.items():
            if states[key].id == state_id:
                storage.delete(states[key])
                storage.save()
                return jsonify({})
        abort(404)
    
