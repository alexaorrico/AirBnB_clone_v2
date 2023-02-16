#!/usr/bin/python3

'''
Create a new view for City objects that handles
all default RestFul API actions.
'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from api.v1.views import get, delete, post, put


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def city_crud(state_id=None, city_id=None):
    '''Returns GET, DELETE, PUT, POST methods'''
    data = {
            'str': 'City',
            '_id': city_id,
            'p_id': state_id,
            'p_prop': 'state_id',
            'p_child': 'cities',
            'p_str': 'State',
            'check': ['name'],
            'ignore': ['created_at', 'updated_at', 'id', 'state_id']}
    methods = {
            'GET': get,
            'DELETE': delete,
            'POST': post,
            'PUT': put
            }
    if request.method in methods:
        return methods[request.method](data)
