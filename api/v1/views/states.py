from models import storage
from models.state import State
from api.v1.views import app_views
from flask import abort, request


@app_views.get('/states')
def states():
    """display all states"""
    return [obj.to_dict() for obj in storage.all(State).values()]


@app_views.get('/states/<id>')
def state_by_id(id):
    """display state by id"""
    state = storage.get(State, id)
    if state:
        return state.to_dict()
    return abort(404)


@app_views.delete('/states/<id>')
def delete_state(id):
    """delete a state by its id"""
    state = storage.get(State, id)
    if state:
        storage.delete(state)
        storage.save()
        return {}
    return abort(404)


@app_views.post('/states', strict_slashes=False)
def create_state():
    """create a new state"""
    if request.is_json:
        data = request.get_json()
        print(data)
        if not data.get('name'):
            return 'Missing name', 400
        new_state = State(**data)
        new_state.save()
        return new_state.to_dict(), 201

    return 'Not a JSON', 400


@app_views.put('/states/<id>')
def update_state(id):
    """update a state by its id"""
    state = storage.get(State, id)
    if not state:
        return abort(404)
    if not request.is_json:
        return 'Not a JSON', 400
    data = request.get_json()
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    storage.save()
    return state.to_dict(), 200
