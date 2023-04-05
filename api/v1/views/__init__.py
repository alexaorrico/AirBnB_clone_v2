#!/usr/bin/python3
from flask import Blueprint, abort
from api.v1.views.index import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

def validate_model(model, model_id):
    """checks if a model exists"""
    from models import storage
    obj = storage.get(model, model_id)
    if obj is None:
        abort(404)
    return obj
