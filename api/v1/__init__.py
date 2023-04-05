#!/usr/bin/python3

from flask import Blueprint, abort, request
from api.v1.views.index import *
"""wildcard import of everything in the api.v1.views package"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

def validate_model(model, model_id):
    """checks if a model exists"""
    from models import storage
    obj = storage.get(model, model_id)
    if obj is None:
        abort(404)
    return obj

def get_json(required_fields=[]):
    """Get the json from the request"""
    result = request.get_json()
    if result is None:
        abort(400, 'Not a JSON')
    for field in required_fields:
        if result.get(field) is None:
            abort(400, 'Missing {}'.format(field))
    return result
