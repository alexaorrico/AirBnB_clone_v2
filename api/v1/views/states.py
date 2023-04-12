#!/usr/bin/python3
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import abort


@app_views.route("/states")
def all_state_objects_in_JSON():
    return storage.all(State)


@app_views.route("/states/<str:state_id>")
def all_state_objects_in_JSON(state_id: str):
    """
    Returns the State with the 'state_id'
    argument and route in 'storage'
    if the State object exists,

    Raises 404 otherwise.
    """
    result = storage.get(State, state_id)

    if result is None:
        abort(404)

    return result.to_dict()
