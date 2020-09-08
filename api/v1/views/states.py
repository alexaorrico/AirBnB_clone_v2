from models.base_model import BaseModel, Base
from flask import jsonify
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def allstates(state_id=None):
    """ jsonify """
    if state_id is None:
        lista = []
        for v in storage.all(State).values():
            lista.append(v.to_dict())
        return (jsonify(lista))
    else:
        for v in storage.all(State).values():
            if v.id == state_id:
                attr = (v.to_dict())
        return (jsonify(attr))


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete(state_id=None):
    if state_id is None:
        return
    for v in storage.all(State).values():
        if v.id == state_id:
            storage.delete(v.id)
            attr = (v.to_dict())
    return (jsonify(attr))
