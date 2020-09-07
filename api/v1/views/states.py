#!/usr/bin/python3
"""
    HBNB_V3: Task 7
"""
from api.v1.views.index import app_views

@app_views.route('/states', strict_slashes=False)
def viewallthestatethings():
    """Retrieves the list of all State objects"""
    from models import storage
    from models.state import State


    stl = storage.all(State)
    li = []
    for state in stl.values():
        li.append(state.to_dict())
    return jsonify(li)
