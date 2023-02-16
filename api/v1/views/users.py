#!/usr/bin/python3

'''
Create a new view for User objects that handles
all default RestFul API actions.
'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from api.v1.views import get, delete, post, put


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user_crud(user_id=None):
    '''Returns GET, DELETE, PUT, POST methods'''
    data = {
            'str': 'User',
            '_id': user_id,
            'p_id': None,
            'check': ['email', 'password'],
            'ignore': ['email', 'created_at', 'updated_at', 'id']}
    methods = {
            'GET': get,
            'DELETE': delete,
            'POST': post,
            'PUT': put
            }
    if request.method in methods:
        return methods[request.method](data)
