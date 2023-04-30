#!/usr/bin/python3

'''
Create a new view for State objects that handles
all default RestFul API actions.
'''

from api.v1.views import app_views, get, delete, post, put
from flask import jsonify, request, abort
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def states_crud(state_id=None):
    '''Returns GET, DELETE, PUT, POST methods'''
    data = {
            'str': 'State',
            '_id': state_id,
            'p_id': None,
            'check': ['name'],
            'ignore': ['created_at', 'updated_at', 'id']
            }
    methods = {
            'GET': get,
            'DELETE': delete,
            'POST': post,
            'PUT': put
            }
    if request.method in methods:
        return methods[request.method](data)
