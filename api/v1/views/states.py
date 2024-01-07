from api.v1.views import app_views
from flask import request


@app_views.route('/states', methods=['GET', 'POST', 'PUT'])
def states():
    """represents the route /status"""
    if request.method == 'GET':
        return {"method": "GET"}
    elif request.method == 'POST':
        return {"method": "POST"}
    elif request.method == 'PUT':
        return {"method": "PUT"}


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def state(state_id):
    """represents the route /status"""
    return {"status": state_id}