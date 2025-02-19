#!/usr/bin/python3
"""
API version 1 views
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State
from api.v1.views.custom import get_cls, delete_cls
from api.v1.views.custom import add_cls, update_cls, handle_E


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
@app_views.route('/states/<cls_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def handle_API_states(cls_id=None):
    """
    returns a cls if cls_id provided, otherwise all clss"""
    cls = State
    if request.method == 'GET':
        return get_cls(cls, cls_id)
    if request.method == 'DELETE':
        return delete_cls(cls, cls_id)
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            return handle_E(message="Not a JSON", code=400)
        if data.get('name') is None:
            return handle_E(message="Missing name", code=400)
        return add_cls(cls, data)
    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return handle_E(message="Not a JSON", code=400)
        if data.get('name') is None:
            return handle_E(message="Missing name", code=400)
        return update_cls(cls, cls_id, data)
