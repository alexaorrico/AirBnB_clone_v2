#!/usr/bin/python3

'''
Create a new view for Review objects that handles
all default RestFul API actions.
'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from api.v1.views import get, delete, post, put


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def review_crud(place_id=None, review_id=None):
    '''Returns GET, DELETE, PUT, POST methods'''
    data = {
            'str': 'Review',
            '_id': review_id,
            'p_id': place_id,
            'p_prop': 'place_id',
            'p_child': 'reviews',
            'p_str': 'Place',
            'check': ['user_id', 'text'],
            'ignore': ['id',
                       'user_id',
                       'place_id',
                       'created_at',
                       'updated_at']}
    methods = {
            'GET': get,
            'DELETE': delete,
            'POST': post,
            'PUT': put
            }
    if request.method in methods:
        return methods[request.method](data)
