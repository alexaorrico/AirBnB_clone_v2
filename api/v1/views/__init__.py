#!/usr/bin/python3
""" Blueprint for API v1 """
from flask import Blueprint, abort, request
from models import storage
# project wants this style
from api.v1.views.index import *


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


def valid_model(model, model_id):
    """ validates if model exists """
    obj = storage.get(model, model_id)
    if obj is None:
        abort(404)
    return obj


def get_json(re_fields=None):
    """ Get json from request """
    if re_fields is None:
        re_fields = []
    result = request.get_json()
    if result is None:
        abort(400, 'Not a JSON')
    for field in re_fields:
        if result.get(field) is None:
            abort(400, 'Missing {}'.format(field))
    return result
