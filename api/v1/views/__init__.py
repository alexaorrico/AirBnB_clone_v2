#!/usr/bin/python
"""Define a blueprint for the API v1"""
from flask import Blueprint, abort

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


def validate_model(model, model_id):
    """Validate if a model exists"""
    from models import storage
    obj = storage.get(model, model_id)
    if obj is None:
        abort(404)
    return obj


# Pep8 doesn't like the next line, project said it's okay
from api.v1.views.index import *
#from api.v1.views.states import *
from api.v1.views.cities import *
