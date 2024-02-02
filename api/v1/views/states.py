from models import storage
from models.state import State
from api.v1.views import app_views
from flask import abort


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


@app_views.post('/states')
def create_state():
    """create a new state"""
    