#!/usr/bin/python3

'''
Create a new view for Amenity objects that handles
all default RestFul API actions.
'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from api.v1.views import get, delete, post, put


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenity_crud(amenity_id=None):
    '''Returns GET, DELETE, PUT, POST methods'''
    data = {
            'str': 'Amenity',
            '_id': amenity_id,
            'p_id': None,
            'check': ['name'],
            'ignore': ['created_at', 'updated_at', 'id']}
    methods = {
            'GET': get,
            'DELETE': delete,
            'POST': post,
            'PUT': put
            }
    if request.method in methods:
        return methods[request.method](data)
